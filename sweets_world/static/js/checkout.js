$(document).ready(function (){


    $('.razor_pay').click( function (e) {
        e.preventDefault();
        var fname=$("[name=firstname]").val();
        var lname=$("[name=lastname]").val();
        var email=$("[name=email]").val();
        var phonenumber=$("[name=phonenumber]").val();
        var address=$("[name=address]").val();
        var city=$("[name=city]").val();
        var country=$("[name=country]").val();
        var state=$("[name=state]").val();
        var token=$("[name='csrfmiddlewaretoken']").val();
        
        

        // to check values are not null//
        if (fname==""|| lname==""|| email==""|| address==""|| phonenumber==""|| city==""|| country==""|| state=="")
        {
            
            swal("Alert!", "All fields are mandatory!", "error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/proceed_to_pay/", 
                success: function (response) {
                    // console.log(response);

                    var options = {
                        "key": "rzp_test_XScqVi0Wvgk5qC", // Enter the Key ID generated from the Dashboard zp_test_bzQxKivDgvku0M
                        "amount": response.grand_total*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Sahal", //your business name
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (response){
                            alert(response.razorpay_payment_id);
                            data={
                                "fname":fname,
                                "lname" :lname,
                               "email":email,
                               "phonenumber":phonenumber,
                               "address":address,
                               "city":city,
                               "country":country,
                               "state": state,
                               "paymentmode":"Paid by Razorpay",
                               "payment_id":response.razorpay_payment_id,
                               csrfmiddlewaretoken:token
                            }
                            $.ajax({
                                method: "POST",
                                url: "/placeorder/",
                                data: "data",
                                
                                success: function (responsec) {  
                                    swal("Congrdulations!", responsec.status, "success").then((value) => {
                                        window.location.href='/my-orders/'
                                        
                                      });               
                                }
                             });

                        },
                        "prefill": { 
                            "name": fname+""+lname, 
                            // "email": email, 
                             "contact": phonenumber 
                        },
                        "notes": {
                            "address": address
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();


                }
           
            });
            

            }

     })

})