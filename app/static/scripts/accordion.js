function w3Show(id, color) {
    let element = $(`#${id}`);
    let showClass = 'w3-show';

    if (element) {
        if (element.hasClass(showClass)) {
            element.removeClass(showClass);
        } else {
            element.addClass(showClass);
        }
    
        if (color) {
            w3SwitchColor(id, color);
        }
    }
}

function w3SwitchColor(id, color) {
    let element = $(`#${id}`);
    let colorClass = `w3-${color}`;

    if (element) {
        if (element.hasClass(colorClass)) {
            element.removeClass(colorClass);
        } else {
            element.addClass(colorClass);
        }
    }
}
