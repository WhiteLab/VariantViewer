/**
 * Created by Miguel on 3/29/17.
 */
$(document).ready(function(){
    /* Set up 'add' modal box */

    new jBox('Modal', {
        attach: $('.igsbviewer-modal-add-button'),
        ajax: {
            url: new_metadata_url
        },
        overlay: true,
        closeOnClick: 'overlay',
        closeButton: 'box'
    });

    /* Set up 'edit' and 'delete' modal boxes */
    var pk = 0;
    var $modalEditButton = $('.igsbviewer-modal-edit-button');
    var $modalDeleteButton = $('.igsbviewer-modal-delete-button');
    $modalEditButton.click(function(){
        pk = $(this).data('pk');
    });
    $modalDeleteButton.click(function(){
        pk = $(this).data('pk');
    });
    new jBox('Modal', {
        onOpen: function(){
            this.options.ajax.url = '/viewer/metadata/edit_metadata/' + pk;
        },
        ajax: {
            reload: true
        },
        attach: $modalEditButton,
        overlay: true,
        closeOnClick: 'overlay',
        closeButton: 'box'
    });
    new jBox('Modal', {
        onOpen: function(){
            this.options.ajax.url = '/viewer/sample/delete_sample/' + pk;
        },
        ajax: {
            reload: true
        },
        attach: $modalDeleteButton,
        overlay: true,
        closeOnClick: 'overlay',
        closeButton: 'box'
    })
});