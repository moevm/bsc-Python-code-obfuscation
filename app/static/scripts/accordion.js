function w3show(id) {
    let x = $(`#${id}`);
    if (x.hasClass('w3-show')) {
        x.removeClass('w3-show');
    } else {
        x.addClass('w3-show');
    }
}
