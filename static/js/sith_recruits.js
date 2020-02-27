$(document).ready(function() {
    $("button.shadowhand").on("click", setShadowHand);
});

async function setShadowHand(event) {
    const target = $(event.target);
    const session = target.attr("data-session");
    const sith = target.attr("data-sith");
    try {
        const response = await axios.get(`/siths/${sith}/shadowhand/set/`, { params: { session } });
        Swal.fire({
            title: 'Успех!',
            text: response.data.message,
            icon: 'success',
            confirmButtonText: 'OK'
        });
        target.remove();
    } catch (error) {
        Swal.fire({
            title: 'Ошибка!',
            text: error.response.data.message,
            icon: 'error',
            confirmButtonText: 'ОК'
        });
    }
}