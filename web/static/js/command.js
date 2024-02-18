const DEBUG = true;

export function initialiseCommands() {
    $('.command-btn').click(function() {
		if ($(this).hasClass('toggleable')) {
			$(this).toggleClass('active inactive');
		}
		if ($(this).hasClass('modal-trigger')) {
			$('#commandModal').modal('show');
			$('#commandModalLabel').text(`Options for ${$(this).text()}`);
		}
	})

}

function log(...args) {
	if (DEBUG)
		console.log("%c[commands.js] ", "color: #FFC300", ...args);
}