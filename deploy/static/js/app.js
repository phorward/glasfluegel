$(document).ready(function () {
    lightbox.option({
      "albumLabel": "Bild %1 von %2"
    });

    // Catalog
    $("div.catalog div.images").on("click",
        function(event)
        {
            var cur = $(this).find("img:visible");
            //alert(cur.length);

            cur.fadeOut();
            var next;

            if( cur.next().length )
                next = cur.next();
            else
                next = $(this).find("img").first();

            next.fadeIn();

            $(this).parent().find("div.info").html("Seite " + next.data("page") + " von " + $(this).find("img").length);
        });

    /* Akkordion! */

    $( ".accordion-toggler").on( "click", function()
    {
        var id = $(this).data( "for-accordion" );

        if( id )
        {
            $(this).children( "span" ).toggleClass( "plus" ).toggleClass( "minus" );
            $( "#" + id ).toggle( 700 );
        }
    });

    $( ".singleton-accordion-toggler").on( "click", function()
    {
        var id = $(this).data( "for-accordion" );

        if( id )
        {
            $( ".singleton-accordion-toggler" ).each( function()
            {
                var span = $(this).children("span");
                var eid = $(this).data( "for-accordion" );

                if( !eid )
                    return;

                if( span.hasClass( "minus" ) )
                {
                    span.removeClass("minus").addClass("plus");
                    $("#" + eid ).hide(700);
                }
                else if( eid == id )
                {
                    span.removeClass("plus").addClass("minus");
                    $("#" + eid ).show(700);
                }
            });
        }
    });


    //Anmeldung
    $("input[name=aircraft]").on("change",
        function(event)
        {
            if(parseInt($(this).val()))
                $("#aircraft_section").fadeIn("slow");
            else
                $("#aircraft_section").fadeOut("slow");
        });

    if(document.getElementById("reg_aircraft_yes") && document.getElementById("reg_aircraft_yes").checked)
        $("#aircraft_section").show();

    $("input[name=camping]").on("change",
        function(event)
        {
            if(parseInt($(this).val()))
                $("#camping_section").fadeIn("slow");
            else
                $("#camping_section").fadeOut("slow");
        });

    if(document.getElementById("reg_camping_yes") && document.getElementById("reg_camping_yes").checked)
        $("#camping_section").show();

    // Bild hochladen! :)
    $("#reg_aircraft_pic_uploader").on("change",
        function(event)
        {
            var files = event.target.files;

            $("#reg_aircraft_pic_loader").fadeIn();
            $("input[type=submit]").attr("disabled", "disabled");

            $.ajax({
                url: "/json/skey",
                dataType: "json"}).done(
                    function( skey )
                    {
                       $.ajax({
                            url: "/json/file/getUploadURL?skey=" + skey,
                            context: document.body
                        }).done(
                           function( uploadUrl )
                           {
                                var data = new FormData();
                                $.each(files, function(key, value)
                                {
                                    data.append(key, value);
                                });

                                $.ajax({
                                    url: uploadUrl,
                                    type: "POST",
                                    data: data,
                                    cache: false,
                                    dataType: "json",
                                    processData: false,
                                    contentType: false,
                                    success: function (data, textStatus, jqXHR) {

                                        $("input[type=submit]").removeAttr("disabled");
                                        $("#reg_aircraft_pic_loader").fadeOut();

                                        if (typeof data.error === 'undefined')
                                        {
                                            var url = data.values[0].servingurl + "=s250";
                                            $("#reg_aircraft_pic").val(data.values[0].key);
                                            $("#reg_aircraft_pic_preview").attr("src", url);
                                            $("#reg_aircraft_pic_preview").fadeIn();
                                        }
                                        else
                                            console.log('ERRORS: ' + data.error);
                                    }
                                });
                            });
                    });
        });


    $("#regform").on("submit",
        function(event)
        {
            var fd = new FormData(event.target);
            var errortxt = "";

            function testField(elem, re)
            {
            	console.log("testField", elem);
                if( !( elem = $("#" + elem) ) )
                {
                    console.error("Field not found");
                    return false;
                }

                if( !elem.val() )
                {
                    if( !errortxt )
                        elem[0].scrollIntoView();

                    var name = $("label[for=" + elem.attr("id") + "]").html();
                    if( name )
                        errortxt += name.replace(" *", "") + " ist ein Pflichtfeld!\n";

                    return false;
                }

                if( re && re !== "undefined" && !re.test(elem.val()))
                {
                    if( !errortxt )
                        elem[0].scrollIntoView();

                    var name = $("label[for=" + elem.attr("id") + "]").html();
                    if( name )
                        errortxt += name.replace(" *", "") + " weist ein ungültiges Format auf.\n";

                    return false;
                }

                return true;
            }

            testField("reg_firstname");
            testField("reg_lastname");
            testField("reg_email", /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
			testField("reg_street");
			testField("reg_zipcode");
			testField("reg_city");
			testField("reg_country");


            if(document.getElementById("reg_aircraft_yes").checked)
            {
                testField("reg_aircraft_type");
                testField("reg_aircraft_reg");
				testField("reg_aircraft_wb");
            }

			if(!document.getElementById("reg_accept_wb").checked)
				errortxt += "Bitte akzeptiere die Wettbewerbsordnung!\n";

			if(!document.getElementById("reg_accept_dsgvo").checked)
				errortxt += "Bitte akzeptiere die Datenschutzvereinbarung!\n";

            if( errortxt )
            {
                $("#regform div.errormessage").html(errortxt.replace(/\n/g, "<br />"));
                $("#regform div.errormessage").fadeIn();
                return false;
            }

            $("#regform div.errormessage").fadeOut();
            //return false;

            $("#formloader").fadeIn();
            $("input[type=submit]").attr("disabled", "disabled");

            $.ajax({
                url: "/json/skey",
                dataType: "json"}).done(
                    function( skey )
                    {
                        $.ajax({
                            url: "/json/reg/add",
                            type: "POST",
                            data: fd,
                            cache: false,
                            dataType: "json",
                            processData: false,
                            contentType: false,
                            success: function (data, textStatus, jqXHR) {

                                $("input[type=submit]").removeAttr("disabled");
                                $("#formloader").fadeOut();

                                if (typeof data.error === 'undefined')
                                {
                                    if( data.action == "addSuccess" )
                                    {
                                        $("#regform")[0].reset();
                                        $("#regform").fadeOut();
                                        $("#regsuccess").fadeIn();
										document.location.hash = "register";
                                    }
                                    else
                                    {
                                        var txt = "";
                                        for( var i = 0; i < data.structure.length; i++ )
                                        {
                                            var fld = data.structure[i][0];

                                            if( data.structure[i][1].error && fld == "email")
                                                txt += data.structure[i][1].descr + " " + data.structure[i][1].error + "\n";
                                            else
                                                continue;

                                            $("#reg_" + fld).addClass("error");
                                        }

                                        alert(txt);
                                    }
                                }
                                else
                                    console.log('ERRORS: ' + data.error);
                            }
                        });
                    });

            return false;
        });

    // Kontaktmailer
    $("#formmailer").on("submit",
        function(event)
        {
            var fd = new FormData(event.target);
            var errortxt = "";

            function testField(elem, re)
            {
                if( !( elem = $("#" + elem) ) )
                {
                    console.log("Not found");
                    return false;
                }

                if( !elem.val() )
                {
                    if( !errortxt )
                        elem[0].scrollIntoView();

                    var name = $("label[for=" + elem.attr("id") + "]").html();
                    if( name )
                        errortxt += name.replace(" *", "") + " ist ein Pflichtfeld!\n";

                    return false;
                }

                if( re && re !== "undefined" && !re.test(elem.val()))
                {
                    if( !errortxt )
                        elem[0].scrollIntoView();

                    var name = $("label[for=" + elem.attr("id") + "]").html();
                    if( name )
                        errortxt += name.replace(" *", "") + " weist ein ungültiges Format auf.\n";

                    return false;
                }

                return true;
            }

            testField("form_email", /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
            testField("form_descr");

            if( !$("#form_privacy").prop("checked") )
            {
                errortxt += "Sie müssen der Verarbeitung Ihrer Daten einwilligen!"
            }

            if( errortxt )
            {
                $("#formmailer div.errormessage").html(errortxt.replace("\n", "<br />"));
                $("#formmailer div.errormessage").fadeIn();
                return false;
            }

            $("#formmailer div.errormessage").fadeOut();
            //return false;

            $("#formloader2").fadeIn();
            $("input[type=submit]").attr("disabled", "disabled");

            $.ajax({
                url: "/json/skey",
                dataType: "json"}).done(
                    function( skey )
                    {
                        $.ajax({
                            url: "/json/contact/add",
                            type: "POST",
                            data: fd,
                            cache: false,
                            dataType: "json",
                            processData: false,
                            contentType: false,
                            success: function (data, textStatus, jqXHR) {

                                $("input[type=submit]").removeAttr("disabled");
                                $("#formloader2").fadeOut();

                                if (typeof data.error === 'undefined')
                                {
                                    if( data.action == "addSuccess" )
                                    {
                                        $("#formmailer")[0].reset();
                                        $("#formmailer").fadeOut();
                                        $("#formmailersuccess").fadeIn();
                                        document.location.hash = "kontakt";
                                    }
                                    else
                                    {
                                        alert("Es trat ein Fehler auf.");
                                    }
                                }
                                else
                                    console.log('ERRORS: ' + data.error);
                            }
                        });
                    });

            return false;
        });

    $("input[type=submit]").removeAttr("disabled");

    // News nachladen
	$("#news-all").on("click",
		function()
		{
			console.log("1");
			$("#news-all").hide();
			$.ajax({
				type: "GET",
				url: "/news/list?cursor=" + $("#news-all").data("cursor") + "&style=next&amount=99&action=1&orderby=creationdate&orderdir=1",
				dataType : 'html',
				cache: false,
				success : function(html){
					console.log("2");
					$("#news-all").parent().append(html);
				}
			});

			return false;
		}
	);
});

