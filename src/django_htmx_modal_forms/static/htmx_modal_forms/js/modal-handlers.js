(() => {
  // Namespace our modal ID to avoid conflicts with other modals
  const MODAL_ID = "htmx-modal-forms-modal";

  // Debug logger setup
  const debug = document.currentScript.getAttribute("data-debug") === "true";
  const log = (...args) => {
    if (debug) {
      console.log("[HTMX Modal]", ...args);
    }
  };
  const error = (...args) => {
    if (debug) {
      console.error("[HTMX Modal]", ...args);
    }
  };

  // Modal utility function
  const getModal = () => {
    const modalEl = document.getElementById(MODAL_ID);
    log("Looking for modal element:", modalEl);

    if (!modalEl) {
      error("Modal element not found!");
      return [null, null];
    }

    // Check if Bootstrap is available
    if (!window.bootstrap) {
      error(
        "Bootstrap is not loaded! Make sure you include Bootstrap JS before this script.",
      );
      return [modalEl, null];
    }

    const bsModal = window.bootstrap.Modal.getOrCreateInstance(modalEl);
    log("Bootstrap modal instance:", bsModal);
    return [modalEl, bsModal];
  };

  // Show modal event handler
  document.addEventListener("modal:show", () => {
    log("modal:show event triggered");
    // Find any existing modals and remove them
    const existingModal = document.getElementById(MODAL_ID);
    if (existingModal) {
      log("Removing existing modal");
      existingModal.remove();
    }

    // Update new modal's ID
    const newModal = document.querySelector(".modal.htmx-added");
    if (newModal) {
      newModal.id = MODAL_ID;
    }

    const [modalEl, bsModal] = getModal();
    if (modalEl && bsModal) {
      log("Showing modal");
      bsModal.show();

      modalEl.addEventListener(
        "hidden.bs.modal",
        () => {
          log("Modal hidden, removing element");
          modalEl.remove();
        },
        { once: true },
      );
    } else {
      error("Could not show modal - missing element or bootstrap instance");
    }
  });

  // Close modal event handler
  document.addEventListener("modal:close", () => {
    log("modal:close event triggered");
    const [modalEl, bsModal] = getModal();

    if (bsModal) {
      log("Hiding modal");
      bsModal.hide();
    } else {
      error("Could not hide modal - missing bootstrap instance");
    }
  });
})();
