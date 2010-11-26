$( document ).ready(function()
{
    // Global
    var HOSTNAME = 'http://' + document.location.host;
    console.debug(HOSTNAME);
    var URLPATH = document.location.pathname;


    /*
    *   This will check the passphrase fields to make sure that both of the 
    *   values that have been entered are the same. So long as they
    *   are not it will show the textbox background as an error color
    */
    $('[name=passphraseCheck]').bind('textchange', function() {
        if ($(this).val() != document.registrationForm.passphrase.value)
        {
            $( this ).addClass( 'fielderror' );
        }
        else
        {
            $( this ).removeClass( 'fielderror' );
        }
    });
        
        
    
    /*
    *   This will bind to the email field, whenever the textbox changes it will check to make
    *   sure that the input is proper for fetching a school. If it is it will fetch the appropraite
    *   school in the background.
    */
    $('[name=email]').bind('textchange', function() {
        var emailString = $(this).val().toString();
        //make sure we have at least five characters in the field. That one of the characters is the '@' symbol, and that the
        //position of the '@' symbol is less then that of the last found instance of .edu
        if ((emailString.length > 5) && (emailString.indexOf('@')!= -1) && (emailString.indexOf('@') < emailString.lastIndexOf('.edu')))
        {
            //We only want to send the server the domain of the email
            emailString = emailString.substring(emailString.indexOf('@'), emailString.length);
            //get the school
            ajaxUniversityEmail(emailString);
        }
        else
        {
            //make sure there isn't any text left in the div
            $('#schoolResponse').text('');
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
                var idArray = []
                var schoolNameArray = []
                var id=''
                var schoolName= ''
    
                if(data.length == 2)
                {
                    $('#schoolResponse').text('Hmm We don\'t seem to have your school on record');

                }
                else
                {
                    $('#schoolResponse').text('');
                    var jsonObject = JSON.parse(data, function(key, value)
                    {
      
                                
                        if(key == 'school')
                        {
                            schoolName = value;
                        }
                        if (key == 'id')
                        {
                            id = value;
                        }
                
                        if (id != '' && schoolName != '')
                        {
                    
                            idArray.push(id);
                            schoolNameArray.push(schoolName);
                            var g ='<input type=\"radio\" name=\"schoolId\" value=\"' + id + '\">'+ schoolName + '<br>';                    
                            id = '';
                            schoolName = '';
                        }
            
                    });

            }            
            if(idArray.length != 0 && idArray.length > 1)
            {
                
                for(var i=0; i < idArray.length; i++)
                {                
                    $('#schoolResponse').append('<input type=\"radio\" name=\"schoolId\" value=\"' + idArray[i] + '\">'+ schoolNameArray[i] + '<br>');
                }
            }
            else
            {
                $('#schoolResponse').append('<input type=\"hidden\" name=\"schoolId\" value=\"' + idArray[0] + '\">' + schoolNameArray[0]+ '<br>');
            }
                           
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

