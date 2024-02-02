
$(document).ready(function() {
    $('.command-btn').click(function() {
        if ($(this).hasClass('toggleable')) {
            $(this).toggleClass('active inactive');
        }
    });
});
// Add to your existing script.js file or inline script tag

$(document).ready(function() {
    console.log("X")
    $('.command-btn').click(function() {
        if ($(this).hasClass('modal-trigger')) {
            $('#commandModal').modal('show');
            // Set the title or content of the modal based on the command
            $('#commandModalLabel').text(`Options for ${$(this).text()}`);
        }
    });
});
