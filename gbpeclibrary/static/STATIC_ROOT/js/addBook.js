$("document").ready(function() {
	$("#addauthor").click( function(e) {
		e.preventDefault();
		$("#authorfield").after(" <div class='row'><div class='col-md-11' id='authorfield'><input type='text' name='akash' class='form-control' placeholder='Author name'></div></div>");
	});
});
