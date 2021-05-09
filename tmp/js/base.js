document.addEventListener('DOMContentLoaded', () => {
	const sidebar = document.querySelector(".sidebar");
	const toggler = document.querySelector(".toggler");

	onWindowResize();

	window.onresize = onWindowResize;
	toggler.addEventListener('click', onClickHandler);
	
	function onWindowResize() {
		if (window.screen.width < 990) {
			const styles = getComputedStyle(sidebar);
			if (styles.marginLeft !== '-250px') {
				onClickHandler();
			}
		}
	}

	function onClickHandler() {
		sidebar.classList.toggle('hide');
		toggler.classList.toggle('rotate');
	}
});