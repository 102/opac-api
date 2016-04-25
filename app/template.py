template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OPAC</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.3/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.6/js/bootstrap.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.6/css/bootstrap.css">
</head>
<body>
<div class="container-fluid" style="padding-top: 15px;">
    <div class="row">
        <div class="col-xs-4">
            <form>
                <div class="form-group">
                    <label>Author</label>
                    <input type="text" class="author form-control" data-name="author"/>
                </div>
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" class="title form-control" data-name="title">
                </div>
                <div class="form-group">
                    <label>Amount</label>
                    <input type="number" class="amount form-control" min="0" data-name="amount"></div>
                <div class="form-group">
                    <label>Offset</label>
                    <input type="number" class="offset form-control" min="0" data-name="offset"></div>
                <button class="search btn btn-default">search</button>
            </form>
        </div>


        <div class="col-xs-8">
            <div class="books-list container">
                <div class="response-data">
                    Total books for query: <span class="total"></span>,
                    books in response: <span class="amount-in-response"></span>
                </div>
                <ol></ol>
            </div>
        </div>

    </div>


</div>
</div>
<script type="text/javascript">
    (function () {
        $('.search').click(function (e) {
            e.preventDefault();
            var params = {};
            $('input').each(function () {
                input = $(this);
                if (input.val()) {
                    params[input.data('name')] = input.val()
                }
            });

            $.get('api?' + $.param(params), function (response) {
                $('.response-data .total').text(response.amount_of_books_for_query);
                $('.response-data .amount-in-response').text(response.amount_of_books_in_response);
                $('.books-list ol').html(null);
                response.books.forEach(function (book) {
                    $('.books-list ol').append('<li>' + book + '</li>');
                })
            })
        })
    })()
</script>
</body>
</html>
"""
