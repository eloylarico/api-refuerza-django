$(function () {
  $(".chat").niceScroll();
});
// Material Select Initialization
$(document).ready(function () {
  $(".mdb-select.validate").materialSelect({
    validate: true,
    labels: {
      validFeedback: "Correct choice",
      invalidFeedback: "Wrong choice",
    },
  });
  function validateSelect(e) {
    e.preventDefault();
    $(".needs-validation").addClass("was-validated");
    if ($(".needs-validation select").val() === null) {
      $(".needs-validation").find(".valid-feedback").hide();
      $(".needs-validation").find(".invalid-feedback").show();
      $(".needs-validation")
        .find(".select-dropdown")
        .val("")
        .prop("placeholder", "No countries selected");
    } else {
      $(".needs-validation").find(".valid-feedback").show();
      $(".needs-validation").find(".invalid-feedback").hide();
    }
  }
  $(".needs-validation select").on("change", (e) => validateSelect(e));
  $(".needs-validation").on("submit", (e) => validateSelect(e));
});
