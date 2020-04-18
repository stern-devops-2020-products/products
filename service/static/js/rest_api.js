$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_description").val(res.description);
        $("#product_category").val(res.category);
        $("#product_sku").val(res.sku);
        $("#product_size").val(res.size);
        $("#product_color").val(res.color);
        $("#product_price").val(res.price);
        $("#product_stock").val(res.stock);
        if (res.available == true) {
            $("#product_available").val("true");
        } else {
            $("#product_available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_description").val("");
        $("#product_category").val("");
        $("#product_sku").val("");
        $("#product_size").val("");
        $("#product_color").val("");
        $("#product_price").val("");
        $("#product_stock").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var available = $("#product_available").val() == "true";
        var description = $("#product_description").val();
        var sku = $("#product_sku").val();
        var size = $("#product_size").val();
        var color = $("#product_color").val();
        var price = $("#product_price").val();
        var stock = $("#product_stock").val();

        var data = {
            "name": name,
            "category": category,
            "available": available,
            "sku": sku,
            "price": price,
            "stock": stock,
            "size": size,
            "color": color,
            "description": description
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product Created")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        var product_id = $("#product_id").val();
        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var available = $("#product_available").val() == "true";
        var description = $("#product_description").val();
        var sku = $("#product_sku").val();
        var size = $("#product_size").val();
        var color = $("#product_color").val();
        var price = $("#product_price").val();
        var stock = $("#product_stock").val();

        var data = {
            "name": name,
            "category": category,
            "available": available,
            "sku": sku,
            "price": price,
            "stock": stock,
            "size": size,
            "color": color,
            "description": description
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/products/" + product_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Product Updated")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Restock a Product
    // ****************************************

    $("#restock-btn").click(function () {

        var product_id = $("#product_id").val();
        var stock = $("#product_stock").val();
        var ajax = $.ajax({
                type: "PUT",
                url: "/products/" + product_id + "?stock=" + stock,
                contentType: "application/json",
                data: ''
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Product Restocked")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/products/" + product_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/products/" + product_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var available = $("#product_available").val() == "true";
        var description = $("#product_description").val();
        var sku = $("#product_sku").val();
        var size = $("#product_size").val();
        var color = $("#product_color").val();
        var price = $("#product_price").val();
        var stock = $("#product_stock").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/products?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:10%">Name</th>'
            header += '<th style="width:10%">SKU</th>'
            header += '<th style="width:10%">Size</th>'
            header += '<th style="width:10%">Price</th>'
            header += '<th style="width:10%">Stock</th>'
            header += '<th style="width:10%">Category</th>'
            header += '<th style="width:10%">Color</th>'
            header += '<th style="width:20%">Description</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            var firstProduct = "";
            for(var i = 0; i < res.length; i++) {
                var product = res[i];
                var row = "<tr><td>"+product.id+"</td><td>"+product.name+"</td><td>"+product.sku+"</td><td>"+product.size+"</td><td>"+product.price+"</td><td>"+product.stock+"</td><td>"+product.category+"</td><td>"+product.color+"</td><td>"+product.description+"</td><td>"+product.available+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstProduct = product;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
