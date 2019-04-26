
    $(document).ready(function () {
        $("#make").click(function() {
            $.ajax({
                url: 'process',
                type: 'POST',
                async: true,
                dataType: 'json',
                data: $('#link').serialize(),
                success: function(data) {
                    document.getElementById('to').innerHTML = '';
                    document.getElementById('to').append(data['response']);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                        document.getElementById('to').innerHTML = xhr.status + " " + thrownError;

                },

            });
        });
    });

