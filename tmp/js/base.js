document.addEventListener('DOMContentLoaded', () => {
	const sidebar = document.querySelector(".sidebar");
	const toggler = document.querySelector(".toggler");

	toggler.addEventListener('click', () => {
		sidebar.classList.toggle('hide');
		toggler.classList.toggle('rotate');
	});

});