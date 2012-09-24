$.extend( $.fn.dataTableExt.oStdClasses, {
    "sWrapper": "dataTables_wrapper form-inline"
} );

function redirectToInspect(options) {
    var url = '';
    if (options.market != 'merge') {
        url += '/' + options.market;
    }

    window.location.href =  url + '/' + options.type + '/' + options.id + '/inspect';
}

function redirectToCompare(options) {
    window.location.href = '/' + options.type + '/' + options.lid + '/compare/' + options.rid;
}


function getSpinner() {
    var opts = {
        lines: 11,
        length: 6,
        width: 1,
        radius: 10,
        rotate: 0,
        color: '#000',
        speed: 1.5,
        trail: 43,
        shadow: true,
        hwaccel: true,
        className: 'spinner',
        zIndex: 2e9,
        top: 'auto',
        left: 'auto'
    };
    return new Spinner(opts).spin();
}

$(document).ready(function() {
    // Home Page
    $('#find-by-id').submit(function(e) {
        e.preventDefault();
        redirectToInspect({
            'id': $('#id').val(),
            'type': $('#type').val(),
            'market': $('#market').val()
        });
        return false;
    });

    $('#compare-by-id').submit(function(e) {
        e.preventDefault();
        redirectToCompare({
            'lid': $('#lid').val(),
            'rid': $('#rid').val(),
            'type': $('#cmp-type').val()
        });
        return false;
    });

    // Search Results Page
    if ($('#search-result-tabs').length) {
        $('#search-result-tabs a:first').tab('show');

        $('.compare-checkbox').click(function(e) {
            if ($('.compare-checkbox:checked').length > 1) {
                $('.compare-checkbox').not(':checked').attr('disabled', true);
            } else {
                $('.compare-checkbox').removeAttr('disabled');
            }
        });

        // BUILD ANOTHER STUPID URL
        $('.comparator').submit(function(e) {
            e.preventDefault();
            if ($('.compare-checkbox:checked').length != 2) {
                alert('Pick two, bro.');
                return false;
            } else {
                var type = $(this).data('type');
                var boxes = $('.compare-checkbox:checked');
                $('#waiting-modal').modal('show');
                window.location.href="/" + type + "/" + $(boxes[0]).val() + '/compare/' + $(boxes[1]).val();
            }
        });
    }

    $('.serp-table').dataTable({
        "sDom": "<'row-fluid'<'span6'l><'span6'>r>t<'row-fluid'<'span6'i><'span6'p>>",
        "sPaginationType": "bootstrap",
        "iDisplayLength": 50
    });


    function getExcludedSections(table) {
        // This is hairy on pages with two tables. Will refactor later.
        var excludedPositions = [];
        table.find('th').each(function() {
            if ($(this).html() != 'Active' && $(this).html() != 'Curation Status' && $(this).html() != 'Status') {
                excludedPositions.push($(this).index());
            }
        });
        return excludedPositions;
    }

    $('.sub-table').each(function(i) {
        $(this).dataTable({
            "sDom": "W<'clear'><'row-fluid'<'span6'l><'span6'>r>t<'row-fluid'<'span6'i><'span6'p>>",
            "sPaginationType": "bootstrap",
            "bFilter": true,
            "bLengthChange": false,
            "iDisplayLength": 50,
            "oColumnFilterWidgets": {
                "aiExclude": getExcludedSections($(this))
            }
        });
    });

    if ($('.confirm-form').length) {
        $('.confirm-form').submit(function(e) {
            e.preventDefault();
            if (confirm('Are you absolutely sure you want to do this?! This is destructive, and probably not recoverable.')) {
                $('#waiting-modal').modal('show');
                spinner = getSpinner();
                $("#waiting-modal #loading").append(spinner.el);
                $(this).off('submit').submit();
            }
        });

        $('.show-delete-btn').click(function() {
            $('.btn-danger').removeClass('hide');
            $(this).parent('label').remove();
        });
    }

    $('.evt-editable').editable({
        success: function() {
            window.location.reload();
        }
    });

    $('.editable-sub, .geolocate-venue').click(function() {
        $('#waiting-modal').modal('show');
    });
});

$(function(){
    // Function to activate the tab
    function activateTab() {
        var activeTab = $('[href=' + window.location.hash.replace('/', '') + ']');
        activeTab && activeTab.tab('show');
    }

    // Trigger when the page loads
    activateTab();

    // Trigger when the hash changes (forward / back)
    $(window).hashchange(function(e) {
        activateTab();
    });

    // Change hash when a tab changes
    $('a[data-toggle="tab"], a[data-toggle="pill"]').on('shown', function () {
        window.location.hash = '/' + $(this).attr('href').replace('#', '');
    });
});