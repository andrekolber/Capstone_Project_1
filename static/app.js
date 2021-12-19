const flashedMsg = document.getElementById('flashed-msgs');

function hideFlashedMsgs() {
	flashedMsg.style.display = 'none';
}

setTimeout(() => {
	hideFlashedMsgs();
}, 3500);

function myFunction() {
	// Declare variables
	let input, filter, table, tr, td, i, txtValue;
	input = document.getElementById('myInput');
	filter = input.value.toUpperCase();
	table = document.getElementById('ticker-table');
	tr = table.getElementsByTagName('tr');

	// Loop through all table rows, and hide those who don't match the search query
	for (i = 0; i < tr.length; i++) {
		td = tr[i].getElementsByTagName('td')[0];
		if (td) {
			txtValue = td.textContent || td.innerText;
			if (txtValue.toUpperCase().indexOf(filter) > -1) {
				tr[i].style.display = '';
			}
			else {
				tr[i].style.display = 'none';
			}
		}
	}
}
