function setVal(val, id) {
    let element = $(`#${id}`);

    if (element) {
        element.val(val);
        element.text(val);
    }
}
