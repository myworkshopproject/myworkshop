'use strict';

import './base.js';
var $ = require("jquery");
var slugify = require('slugify');

function createUsername() {
    let first_name = $("#id_first_name").val();
    let last_name = $("#id_last_name").val();
    let matches = slugify(first_name).match(/\b(\w)/g) || [' '];
    let first_name_initials = matches.join('');
    let full_name = first_name_initials + last_name;
    $("#id_username").val(slugify(full_name, {
        replacement: '', // replace spaces with replacement character, defaults to `-`
        remove: undefined, // remove characters that match regex, defaults to `undefined`
        lower: true, // convert to lower case, defaults to `false`
        strict: true, // strip special characters except replacement, defaults to `false`
        locale: 'vi', // language code of the locale to use
        trim: true // trim leading and trailing replacement chars, defaults to `true`
    }));
}

$("#id_first_name, #id_last_name").keyup(function() {
    createUsername();
});

// if you want this function to run when the page loads,
// just call the function once outside of the keyup event
// createUsername();
