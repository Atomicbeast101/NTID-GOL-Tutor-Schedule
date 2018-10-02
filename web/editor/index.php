<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title>NTID GOL Lab - Tutors</title>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script>
        <script src='../assets/js/main.js'></script>
        <link rel="stylesheet" href="../assets/css/main.css">
    </head>
    <body>
        <?php
            $hostname = "129.21.218.105";
            $colors = array(
                "green",
                "dark_green",
                "gray",
                "brown",
                "red",
                "yellow",
                "cyan",
                "brown",
                "blue",
                "dark_blue",
                "purple",
                "dark_purple",
                "pink",
                "dark_pink",
                "orange",
                "dark_orange",
                "lime",
                "dark_lime"
            );

            //error_reporting(E_ALL);
            //ini_set('display_errors', 1);

            function show_alert($json) {
                $data = json_decode($json);
                if($data->status == 'success')
                    echo("<script>alert('SUCCESS');</script>");
                else
                    echo("<script>alert('" . $data->reason . "');</script>");
            }

            if(isset($_POST['form_type'])) {
                $form_type = $_POST['form_type'];
                if($form_type == 'ADD_TUTOR') {
                    $name = ucfirst($_POST['first_name']) . '_' . ucfirst($_POST['last_name']);
                    $color = $_POST['color'];
                    $position = $_POST['position'];
                    $email = $_POST['email'];
                    $major = $_POST['major'];
                    $data = array(
                        'name' => $name,
                        'color' => $color,
                        'position' => $position,
                        'email' => $email,
                        'major' => $major
                    );
                    if(isset($_POST['skills'])) {
                        $skills = implode(",", $_POST['skills']);
                        $data['skills'] = $skills;
                    }
                    
                    $data = http_build_query($data);
                    $result = file_get_contents('http://' . $hostname . ':9001/add_tutor?' . $data);
                    show_alert($result);
                }
                else if($form_type == 'REMOVE_TUTOR') {
                    $name = str_replace(' ', '_', $_POST['full_name']);
                    $data = array(
                        'name' => $name
                    );
                    
                    $data = http_build_query($data);
                    $result = file_get_contents('http://' . $hostname . ':9001/remove_tutor?' . $data);
                    show_alert($result);
                }
                else if($form_type == 'MODIFY_TUTOR') {
                    $name = str_replace(' ', '_', $_POST['full_name']);
                    $color = $_POST['color'];
                    $position = $_POST['position'];
                    $email = $_POST['email'];
                    $major = $_POST['major'];
                    $data = array(
                        'name' => $name,
                        'color' => $color,
                        'position' => $position,
                        'email' => $email,
                        'major' => $major
                    );
                    if(isset($_POST['skills'])) {
                        $skills = implode(",", $_POST['skills']);
                        $data['skills'] = $skills;
                    }

                    $data = http_build_query($data);
                    $result = file_get_contents('http://' . $hostname . ':9001/modify_tutor?' . $data);
                    show_alert($result);
                }
                else if($form_type == 'ADD_SKILL') {
                    $skill = $_POST['skill'];
                    
                    $data = http_build_query(array(
                        'skill' => $skill
                    ));
                    $result = file_get_contents('http://' . $hostname . ':9001/add_skill?' . $data);
                    show_alert($result);
                }
                else if($form_type == 'REMOVE_SKILL') {
                    $skill = $_POST['skill'];
                    
                    $data = http_build_query(array(
                        'skill' => $skill
                    ));
                    $result = file_get_contents('http://' . $hostname . ':9001/remove_skill?' . $data);
                    show_alert($result);
                }
                else if($form_type == 'UPDATE_CALENDAR') {
                    $days = array(
                        'sun',
                        'mon',
                        'tue',
                        'wed',
                        'thu',
                        'fri'
                    );
                    $mon_thu_times = array(
                        '10-11',
                        '11-12',
                        '12-01',
                        '01-02',
                        '02-03',
                        '03-04',
                        '04-05',
                        '05-06',
                        '06-07',
                        '07-08',
                        '08-09'
                    );
                    $fri_times = array(
                        '10-11',
                        '11-12',
                        '12-01',
                        '01-02',
                        '02-03',
                        '03-04',
                        '04-05'
                    );
                    $sun_times = array(
                        '02-03',
                        '03-04',
                        '04-05',
                        '05-06'
                    );
                    $data = array();
                    foreach($days as $day) {
                        if($day != 'fri' && $day != 'sun') {
                            foreach($mon_thu_times as $time) {
                                $shift = $day . '_' . $time;
                                if(isset($_POST[$shift]))
                                    $data[$shift] = implode(",", $_POST[$shift]);
                            }
                        }
                        else if($day == 'fri') {
                            foreach($fri_times as $time) {
                                $shift = $day . '_' . $time;
                                if(isset($_POST[$shift]))
                                    $data[$shift] = implode(",", $_POST[$shift]);
                            }
                        }
                        else if($day == 'sun') {
                            foreach($sun_times as $time) {
                                $shift = $day . '_' . $time;
                                if(isset($_POST[$shift]))
                                    $data[$shift] = implode(",", $_POST[$shift]);
                            }
                        }
                    }

                    $data = http_build_query($data);
                    $result = file_get_contents('http://' . $hostname . ':9001/update_week_schedule?' . $data);
                    show_alert($result);
                }
            }
        ?>
        <header>
            <div class='left'>
                <h1>NTID GOL Lab Editor</h1>
            </div>
            <div class='right'>
                <a href='../index.html'>Home</a>
            </div>
        </header>
        <div id='editor'>
            <div id='add-tutor' class='editor-box'>
                <h3>Add New Tutor</h3>
                <form action='<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>' method='post'>
                    <input type='hidden' name='form_type' value='ADD_TUTOR' />
                    <input type='text' placeholder='First Name' name='first_name' required>
                    <input type='text' placeholder='Last Name' name='last_name' required>
                    <select name='color'>
                        <?php
                            foreach($colors as $color) {
				print("<option>" . $color . "</option>");
                            }
                        ?>
                    </select>
                    <select name='position'>
                        <option>Student Tutor</option>
                        <option>Student Tutor Leader</option>
                        <option>Faculty Tutor</option>
                    </select>
                    <input type='email' placeholder='user@example.com' name='email' required>
                    <input type='text' placeholder='Major' name='major' required>
                    <select id='add_tutor_skills' name='skills[]' multiple></select>
                    <button class='func' type='submit'>Add</button>
                </form>
            </div>
            <div id='remove-tutor' class='editor-box'>
                <h3>Remove Tutor</h3>
                <form action='<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>' method='post'>
                    <input type='hidden' name='form_type' value='REMOVE_TUTOR' />
                    <select id='remove_tutor_name' name='full_name'></select>
                    <button class='func' type='submit'>Remove</button>
                </form>
            </div>
            <div id='modify-tutor' class='editor-box'>
                <h3>Modify A Tutor</h3>
                <form action='<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>' method='post'>
                    <input type='hidden' name='form_type' value='MODIFY_TUTOR' />
                    <select id='modify_tutor_name' onchange='get_tutor_info()' name='full_name'></select>
                    <select id='modify_tutor_color' name='color'>
                        <?php
                            foreach($colors as $color) {
                                print("<option>" . $color . "</option>");
                            }
                        ?>
                    </select>
                    <select id='modify_tutor_position' name='position'>
                        <option>Student Tutor</option>
                        <option>Student Tutor Leader</option>
                        <option>Faculty Tutor</option>
                    </select>
                    <input type='text' placeholder='email' name='email' id='modify_tutor_email' />
                    <input type='text' placeholder='major' name='major' id='modify_tutor_major' />
                    <select id='modify_tutor_skills' name='skills[]' multiple></select>
                    <button class='func' type='submit'>Update</button>
                </form>
            </div>
            <br />
            <div id='add-skill' class='editor-box'>
                <h3>Add New Skill</h3>
                <form action='<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>' method='post'>
                    <input type='hidden' name='form_type' value='ADD_SKILL' />
                    <input type='text' placeholder='Skill' name='skill' />
                    <button class='func' type='submit'>Add</button>
                </form>
            </div>
            <div id='remove-skill' class='editor-box'>
                <h3>Remove Skill</h3>
                <form action='<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>' method='post'>
                    <input type='hidden' name='form_type' value='REMOVE_SKILL' />
                    <select id='remove_skill_list' name='skill'></select>
                    <button class='func' type='submit'>Remove</button>
                </form>
            </div>
            <br />
            <div id='set-schedule' class='editor-box'>
                <h3>Update Tutor Schedule</h3>
                <form action='<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>' method='post'>
                    <input type='hidden' name='form_type' value='UPDATE_CALENDAR' />
                    <table id='load_schedule'>
                        <tr>
                            <th class='time-block'></th>
                            <th>Sunday</th>
                            <th>Monday</th>
                            <th>Tuesday</th>
                            <th>Wednesday</th>
                            <th>Thursday</th>
                            <th>Friday</th>
                            <th class='sat-block'>Saturday</th>
                        </tr>
                    </table>
                    <script>
                        var days = [
                            'sun',
                            'mon',
                            'tue',
                            'wed',
                            'thu',
                            'fri'
                        ];
                        var times = [
                            { 'time':'10-11', 'label':'10-11am' },
                            { 'time':'11-12', 'label':'11-12pm' },
                            { 'time':'12-01', 'label':'12-1pm' },
                            { 'time':'01-02', 'label':'1-2pm' },
                            { 'time':'02-03', 'label':'2-3pm' },
                            { 'time':'03-04', 'label':'3-4pm' },
                            { 'time':'04-05', 'label':'4-5pm' },
                            { 'time':'05-06', 'label':'5-6pm' },
                            { 'time':'06-07', 'label':'6-7pm' },
                            { 'time':'07-08', 'label':'7-8pm' },
                            { 'time':'08-09', 'label':'8-9pm' }
                        ];

                        for(var time in times) {
                            var chunk = '';
                            chunk += '<td class="time-block">' + times[time]['label'] + '</td>';
                            for(var day in days)
                                chunk += '<td><select id="' + days[day] + '_' + times[time]['time'] + '" name="' + days[day] + '_' + times[time]['time'] + '[]" multiple></select></td>';
                            chunk += '<td class="sat-block"></td>';
                            document.getElementById('load_schedule').innerHTML += chunk;
                        }
                    </script>
                    <button class='func' type='submit'>Update</button>
                </form>
            </div>
        </div>
        <script>
            try {
                var tutors = [];
                var skills = [];

                // Get tutor names
                $.getJSON('http://<?php echo $hostname; ?>:9000/all_tutors_name', function(data) {
                    if(data['status'] == 'success') {
                        for(var tutor in data['data'])
                            tutors.push(data['data'][tutor]);
                        
                        tutors.forEach(function(tutor) {
                            var name = tutor.replace('_', ' ');
                            document.getElementById('remove_tutor_name').innerHTML += '<option>' + name + '</option>';
                            document.getElementById('modify_tutor_name').innerHTML += '<option>' + name + '</option>';
                        });
                        document.getElementById('remove_tutor_name').innerHTML += '<option disabled selected value>- Select Name -</option>';
                        document.getElementById('modify_tutor_name').innerHTML += '<option disabled selected value>- Select Name -</option>';
                    }
                });

                // Get skills
                $.getJSON('http://<?php echo $hostname; ?>:9000/all_skills', function(data) {
                    if(data['status'] == 'success') {
                        for(var skill in data['data'])
                            skills.push(data['data'][skill]);
                        
                        skills.forEach(function(skill) {
                            document.getElementById('add_tutor_skills').innerHTML += '<option>' + skill + '</option>';
                            document.getElementById('modify_tutor_skills').innerHTML += '<option>' + skill + '</option>';
                            document.getElementById('remove_skill_list').innerHTML += '<option>' + skill + '</option>';
                        });
                        document.getElementById('remove_skill_list').innerHTML += '<option disabled selected value>- Select Skill -</option>';
                    }
                });

                // Get schedule
                $.getJSON('http://<?php echo $hostname; ?>:9000/weekly_schedule', function(data) {
                    if(data['status'] == 'success') {
                        times.forEach(function eachTime(time, time_index) {
                            for(var day in days) {
                                var element = document.getElementById(days[day] + '_' + time.time);
                                for(var tutor in tutors) {
                                    var name = tutors[tutor];
                                    var added = false;
                                    if(data['data'][days[day] + '_' + time.time]['tutor_1']['name'] != '') {
                                        if(data['data'][days[day] + '_' + time.time]['tutor_1']['name'] == name) {
                                            added = true;
                                            element.innerHTML += '<option selected>' + name.replace('_', ' ') + '</option>';
                                        }
                                    }
                                    if(data['data'][days[day] + '_' + time.time]['tutor_2']['name'] != '') {
                                        if(data['data'][days[day] + '_' + time.time]['tutor_2']['name'] == name) {
                                            added = true;
                                            element.innerHTML += '<option selected>' + name.replace('_', ' ') + '</option>';
                                        }
                                    }
                                    if(!added)
                                        element.innerHTML += '<option>' + name.replace('_', ' ') + '</option>';
                                }
                                
                            }
                        });
                    }
                });
            }
            catch(Exception) {
                console.log('ERROR: Unable to access server!');
            }
        </script>
        <footer>
            Copyright &copy; RIT/NTID GOL Lab. All Rights Reserved. Developed & Maintained by Adam Brodack.
        </footer>
    </body>
</html>
