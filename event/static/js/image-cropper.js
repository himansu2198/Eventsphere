/**
 * ImageCropper — reusable crop-before-upload component.
 *
 * Usage:
 *   ImageCropper.attach({
 *     inputId: 'id_logo',        // the existing <input type="file">
 *     ratio: 9 / 4,              // fixed crop aspect ratio (width / height)
 *     outputWidth: 720,          // exported image pixel width
 *     outputHeight: 320,         // exported image pixel height
 *     previewId: 'logoPreview',  // optional <img> to show the cropped result
 *   });
 *
 * No backend changes needed: the cropped result is converted to a real
 * File object and assigned back onto the SAME <input>, so Django's
 * request.FILES.get('logo') works completely unchanged.
 */
const ImageCropper = (function () {
  let modalEl, imageEl, cropperInstance, activeConfig;

  function ensureModal() {
    if (document.getElementById('imageCropperModal')) return;

    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
      <div class="modal fade" id="imageCropperModal" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title"><i class="bi bi-crop"></i> Crop Image</h5>
              <button type="button" class="btn-close" id="cropperCancelX"></button>
            </div>
            <div class="modal-body">
              <div class="crop-image-wrapper">
                <img id="cropperTargetImage" src="" alt="Crop preview">
              </div>
              <div class="crop-controls mt-3">
                <button type="button" class="btn btn-sm btn-outline-secondary" id="cropZoomOut"><i class="bi bi-zoom-out"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" id="cropZoomIn"><i class="bi bi-zoom-in"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" id="cropReset"><i class="bi bi-arrow-counterclockwise"></i> Reset</button>
                <span class="text-muted ms-2" style="font-size:0.78rem;">Drag to reposition, use buttons or scroll to zoom.</span>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" id="cropperCancelBtn">Cancel</button>
              <button type="button" class="btn btn-primary" id="cropperApplyBtn"><i class="bi bi-check-lg"></i> Apply Crop</button>
            </div>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(wrapper.firstElementChild);

    modalEl = document.getElementById('imageCropperModal');
    imageEl = document.getElementById('cropperTargetImage');

    document.getElementById('cropZoomIn').addEventListener('click', () => cropperInstance && cropperInstance.zoom(0.1));
    document.getElementById('cropZoomOut').addEventListener('click', () => cropperInstance && cropperInstance.zoom(-0.1));
    document.getElementById('cropReset').addEventListener('click', () => cropperInstance && cropperInstance.reset());
    document.getElementById('cropperApplyBtn').addEventListener('click', applyCrop);
    document.getElementById('cropperCancelBtn').addEventListener('click', cancelCrop);
    document.getElementById('cropperCancelX').addEventListener('click', cancelCrop);
  }

  function openForInput(config, file) {
    activeConfig = config;
    ensureModal();

    const reader = new FileReader();
    reader.onload = function (e) {
      imageEl.src = e.target.result;
      const bsModal = new bootstrap.Modal(modalEl);
      bsModal.show();

      modalEl.addEventListener('shown.bs.modal', function onceShown() {
        modalEl.removeEventListener('shown.bs.modal', onceShown);
        if (cropperInstance) cropperInstance.destroy();
        cropperInstance = new Cropper(imageEl, {
          aspectRatio: config.ratio,
          viewMode: 1,
          dragMode: 'move',
          autoCropArea: 1,
          background: false,
          responsive: true,
          guides: true,
        });
      });
    };
    reader.readAsDataURL(file);
  }

  function applyCrop() {
    if (!cropperInstance || !activeConfig) return;

    cropperInstance.getCroppedCanvas({
      width: activeConfig.outputWidth || 800,
      height: activeConfig.outputHeight || Math.round((activeConfig.outputWidth || 800) / activeConfig.ratio),
      imageSmoothingQuality: 'high',
    }).toBlob(function (blob) {
      const inputEl = document.getElementById(activeConfig.inputId);
      const originalFile = inputEl.files[0];
      const fileName = originalFile ? originalFile.name.replace(/\.[^.]+$/, '') + '-cropped.jpg' : 'cropped.jpg';
      const croppedFile = new File([blob], fileName, { type: 'image/jpeg' });

      const dt = new DataTransfer();
      dt.items.add(croppedFile);
      inputEl.files = dt.files;

      if (activeConfig.previewId) {
        const previewEl = document.getElementById(activeConfig.previewId);
        if (previewEl) {
          previewEl.src = URL.createObjectURL(croppedFile);
          previewEl.style.display = '';
        }
      }

      closeModal();
    }, 'image/jpeg', 0.92);
  }

  function cancelCrop() {
    if (activeConfig) {
      const inputEl = document.getElementById(activeConfig.inputId);
      inputEl.value = '';
    }
    closeModal();
  }

  function closeModal() {
    if (cropperInstance) {
      cropperInstance.destroy();
      cropperInstance = null;
    }
    const bsModal = bootstrap.Modal.getInstance(modalEl);
    if (bsModal) bsModal.hide();
  }

  function attach(config) {
    const inputEl = document.getElementById(config.inputId);
    if (!inputEl) return;

    inputEl.addEventListener('change', function () {
      const file = inputEl.files[0];
      if (file) {
        openForInput(config, file);
      }
    });
  }

  return { attach };
})();