'use strict';

import './css/base.css';
import './bulma.js';
import './fontawesome.js';

// favicon
import favicon from './img/tools-solid.svg';
const link = document.createElement('link');
link.rel = 'shortcut icon';
link.href = favicon;
document.head.appendChild(link);

var simplemde = require('simplemde');
import 'simplemde/dist/simplemde.min.css';

new simplemde({
    element: document.getElementById("id_source"),
    hideIcons: [
        "image",
        "preview",
        "side-by-side",
        "fullscreen",
        "guide",
        "heading"
    ],
    showIcons: [
        "heading-2",
        "heading-3",
        "code",
        "table",
        "horizontal-rule"
    ],
});
