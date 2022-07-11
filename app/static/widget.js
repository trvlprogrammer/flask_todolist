function hideSelected(value) {
    if (value && !value.selected) {
      return $('<span>' + value.text + '</span>');
    }
  }

  $(document).ready(function() {
    $('.widget-many2many-tags').select2({
      allowClear: true,
      placeholder: {
        id: "",
        placeholder: "Tags"
      },
      minimumResultsForSearch: -1,
      templateResult: hideSelected,
    });
  });

