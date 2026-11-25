// Auto-dismiss flash alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => {
      try { new bootstrap.Alert(el).close(); } catch(e) {}
    });
  }, 4000);
});
