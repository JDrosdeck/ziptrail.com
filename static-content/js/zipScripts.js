$( document ).ready(function()
{
    // Global
    var HOSTNAME = 'http://' + document.location.host;
    console.debug(HOSTNAME);
    var URLPATH = document.location.pathname;



    $('[name=passphraseCheck]').bind('textchange', function() {
        if ($(this).val() != document.registrationForm.passphrase.value)
        {
         $( this ).addClass( 'fielderror' );
        }
        else{
            $( this ).removeClass( 'fielderror' );
        }
        });
        
        





    //Bind to the email field and check for valid input
    //also fetch the schools that the user might belong to
    $('[name=email]').bind('textchange', function() {
        var emailString = $(this).val().toString();
        //make sure we have at least five characters in the field. That one of the characters is the '@' symbol, and that the
        //position of the '@' symbol is less then that of the last found instance of .edu
        if ((emailString.length > 5) && (emailString.indexOf('@')!= -1) && (emailString.indexOf('@') < emailString.lastIndexOf('.edu')))
        {
            emailString = emailString.substring(emailString.indexOf('@'), emailString.length);
            ajaxUniversityEmail(emailString);
        }
        });
    
    /* 
    * Function ajaxUniversityEmail
    * calls the server and returns the school(s)
    * that the email belongs to
    */
    function ajaxUniversityEmail(email) {
        $.ajax({url: HOSTNAME + '/checkEmail/', type:'Get', cache:false,
            data : {
                email:email
            },
            success: function(data) {
                //This should have a JSON string with all the schools
                //that have that email address
                
                var jsonObject = JSON.parse(data, function(key, value){
                
                    if(key == 'school')
                    {
                        $('#schoolResponse').text(value);
                    }
                }
            );
              //  alert(data)
            }});
    };







    // Validate email address for university
    $('[name=email]').bind('textchange', function () {

        if( isValidEmail( $( this ).val() ) )
            $( this ).removeClass( 'fielderror' );
        else
            $( this ).addClass( 'fielderror' );
    });

    $('[name=email]').bind('notext', function () {
        $( this ).removeClass( 'fielderror' );
    });    

    /**
        * BRIEF: Validates an email address
        * 
        * SOURCE: 
        * Pattern by James Watts and Francisco Jose Martin Moreno
        * http://fightingforalostcause.net/misc/2006/compare-email-regex.php
        *
        * RETURNS: 
        * boolean validation status
        */
    function isValidEmail( address ) {
        var pattern = new RegExp(/^([\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+\.)*[\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+@((((([a-z0-9]{1}[a-z0-9\-]{0,62}[a-z0-9]{1})|[a-z])\.)+[a-z]{2,6})|(\d{1,3}\.){3}\d{1,3}(\:\d{1,5})?)$/i);
            return pattern.test( address );
        }



});

