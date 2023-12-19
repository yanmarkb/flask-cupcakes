async function getCupcakes() {
	const response = await axios.get("/api/cupcakes");
	for (let cupcake of response.data.cupcakes) {
		$("#cupcakes-list").append(`
            <li>
                <img src="${cupcake.image}" alt="Cupcake Image" width="50" height="50">
                ${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}
                <button class="delete" data-id="${cupcake.id}">Delete</button>
            </li>
        `);
	}
}

$("#new-cupcake-form").on("submit", async function (event) {
	event.preventDefault();

	const flavor = $("#flavor").val();
	const size = $("#size").val();
	const rating = $("#rating").val();
	const image = $("#image").val();

	const response = await axios.post("/api/cupcakes", {
		flavor,
		size,
		rating,
		image,
	});

	$("#cupcakes-list").append(`
        <li>
            <img src="${response.data.cupcake.image}" alt="Cupcake Image" width="50" height="50">
            ${response.data.cupcake.flavor} - ${response.data.cupcake.size} - ${response.data.cupcake.rating}
        </li>
    `);
});

getCupcakes();

$("#cupcakes-list").on("click", ".delete", async function (event) {
	const id = $(event.target).data("id");
	await axios.delete(`/api/cupcakes/${id}`);
	$(event.target).parent().remove();
});
