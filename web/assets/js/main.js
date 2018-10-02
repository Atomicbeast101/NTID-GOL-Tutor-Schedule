// Variables
var ip_address = '<REMOVED>';
var success = false;


// Get tutor info
function get_tutor_info() {
    try {
        var element = document.getElementById('modify_tutor_name');
        var name = element.options[element.selectedIndex].text;
        $.getJSON('http://' + ip_address + ':9000/get_tutor/' + name.replace(' ', '_'), function(data) {
            if(data['status'] == 'success') {
                document.getElementById('modify_tutor_color').value = data['data']['color'];
                document.getElementById('modify_tutor_position').value = data['data']['position'];
                document.getElementById('modify_tutor_email').value = data['data']['email'];
                document.getElementById('modify_tutor_major').value = data['data']['major'];
                var skills = [];
                for(var skill in data['data']['skills'])
                    skills.push(data['data']['skills'][skill]);
                var ele = document.getElementById('modify_tutor_skills');
                for(var i = 0; i < ele.options.length; i++) {
                    var option = ele.options[i];
                    if(skills.indexOf(option.text) != -1) {
                        option.selected = true;
                    }
                }
            }
        });
    }
    catch(Exception) {
        console.log('ERROR: Unable to access server!');
        success = false;
    }
}
function imageExists(image_url){
    var http = new XMLHttpRequest();
    http.open('HEAD', image_url, false);
    http.send();
    return http.status != 404;
}


// Update Calendar
function create_html(tutor_data) {
    if(tutor_data['num_tutors'] == 0)
        return '<div class="blank"></div>';

    else if(tutor_data['num_tutors'] == 1)
        return '<div class="' + tutor_data['tutor_1']['color'] + '">' + tutor_data['tutor_1']['name'].replace('_', ' ') + '</div>';

    else
        return '<div class="' + tutor_data['tutor_1']['color'] + ' half left">' + tutor_data['tutor_1']['name'].replace('_', ' ') + '</div><div class="' + tutor_data['tutor_2']['color'] + ' half right">' + tutor_data['tutor_2']['name'].replace('_', ' ') + '</div>';
}
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
]
function updateCalendar() {
	success = false;
	try {
	    $.getJSON('http://129.21.218.105:9000/weekly_schedule', function(data) {
		if(data['status'] == 'success') {
		    document.getElementById('week-schedule').innerHTML = '';
		    success = true;
		    var chunk = '<tr>';
		    chunk += '<th class="time-block"></th>';
		    chunk += '<th>Sunday</th>';
		    chunk += '<th>Monday</th>';
		    chunk += '<th>Tuesday</th>';
		    chunk += '<th>Wednesday</th>';
		    chunk += '<th>Thursday</th>';
		    chunk += '<th>Friday</th>';
		    chunk += '<th class="sat-block">Saturday</th>';
		    chunk += '</tr>';
		    document.getElementById('week-schedule').innerHTML += chunk;
		    times.forEach(function eachTime(time, time_index) {
		        chunk = '';
		        chunk += '<tr>';
		        chunk += '    <td class="time-block">' + time.label + '</td>';
		        chunk += '    <td class="tutor">' + create_html(data['data']['sun_' + time.time]) + '</td>';
		        chunk += '    <td class="tutor">' + create_html(data['data']['mon_' + time.time]) + '</td>';
		        chunk += '    <td class="tutor">' + create_html(data['data']['tue_' + time.time]) + '</td>';
		        chunk += '    <td class="tutor">' + create_html(data['data']['wed_' + time.time]) + '</td>';
		        chunk += '    <td class="tutor">' + create_html(data['data']['thu_' + time.time]) + '</td>';
		        chunk += '    <td class="tutor">' + create_html(data['data']['fri_' + time.time]) + '</td>';
		        chunk += '    <td class="sat-block"></td>';
		        chunk += '</tr>';
		        document.getElementById('week-schedule').innerHTML += chunk;
		    });
		}
	    });
	}
	catch(err) {
	    console.log('ERROR: Unable to access server!');
	    success = false;
	}
	if(!success) {
	    document.getElementById('week-schedule').innerHTML = '';
	    var chunk = '<tr>';
	    chunk += '    <th class="time-block"></th>';
	    chunk += '    <th>Sunday</th>';
	    chunk += '    <th>Monday</th>';
	    chunk += '    <th>Tuesday</th>';
	    chunk += '    <th>Wednesday</th>';
	    chunk += '    <th>Thursday</th>';
	    chunk += '    <th>Friday</th>';
	    chunk += '    <th class="sat-block">Saturday</th>';
	    chunk += '</tr>';
	    document.getElementById('week-schedule').innerHTML += chunk;
	    times.forEach(function eachTime(time, time_index) {
		chunk = '';
		chunk += '<tr>';
		chunk += '    <td class="time-block">' + time.label + '</td>';
		chunk += '    <td class="tutor"><div class="blank red">ERROR</div></td>';
		chunk += '    <td class="tutor"><div class="blank red">ERROR</div></td>';
		chunk += '    <td class="tutor"><div class="blank red">ERROR</div></td>';
		chunk += '    <td class="tutor"><div class="blank red">ERROR</div></td>';
		chunk += '    <td class="tutor"><div class="blank red">ERROR</div></td>';
		chunk += '    <td class="tutor"><div class="blank red">ERROR</div></td>';
		chunk += '    <td class="sat-block"></td>';
		chunk += '</tr>';
		document.getElementById('week-schedule').innerHTML += chunk;
	    });
	}
}


// Update time
window.setInterval(function(){
    var now = new Date();
    var isPM = now.getHours() >= 12;
    var isMidday = now.getHours() == 12;
    var hour = now.getHours() - (isPM && !isMidday ? 12 : 0);
    var minute = (now.getMinutes()<10?'0':'') + now.getMinutes();
    var second = (now.getSeconds()<10?'0':'') + now.getSeconds();
    var tt = (isPM ? ' PM' : ' AM');
    var time = [hour, minute, second].join(":") + tt;
    document.getElementById('time').innerHTML = "<h3>" + time + "</h3>";
}, 1000);


// Update Lab Status
function updateLabStatus() {
	success = false;
	try {
	    $.getJSON('http://129.21.218.105:9000/lab_open', function(data) {
		if(data['status'] == 'success') {
		    success = true;
		    if(data['data']['open'] == true) {
		        document.getElementById('lab-status').className = 'open';
		        document.getElementById('lab-status').innerHTML = '<h3>Tutor Lab Open</h3>';
		    }
		    else {
		        document.getElementById('lab-status').className = 'closed';
		        document.getElementById('lab-status').innerHTML = '<h3>Tutor Lab Closed</h3>';
		    }
		}
	    });
	}
	catch(Exception) {
	    console.log('ERROR: Unable to access server!');
	    success = false;
	}
	if(!success) {
	    document.getElementById('lab-status').className = 'closed';
	    document.getElementById('lab-status').innerHTML = '<h3>ERROR</h3>';
	}
}

// Update Current Tutor Info
function updateCurrentTutor() {
	success = false;
	try {
	    $.getJSON('http://' + ip_address + ':9000/get_current_tutors', function(data) {
		if(data['status'] == 'success') {
		    success = true;
		    if(data['data']['open'] == true) {
		        document.getElementById('tutor_1_color').className = 'tutor-color ' + data['data']['tutor_1']['color'];
		        document.getElementById('tutor_2_color').className = 'tutor-color ' + data['data']['tutor_2']['color'];
		        var tutor1_img = 'assets/img/' + data['data']['tutor_1']['name'] + '.jpg';
		        if(imageExists(tutor1_img))
		            document.getElementById('tutor_1_img').src = tutor1_img;
		        else
		            document.getElementById('tutor_1_img').src = 'assets/img/example_profile.jpg';
			var tutor2_img = 'assets/img/' + data['data']['tutor_2']['name'] + '.jpg';
		        if(imageExists(tutor2_img))
		            document.getElementById('tutor_2_img').src = tutor2_img;
		        else
		            document.getElementById('tutor_2_img').src = 'assets/img/example_profile.jpg';                                
		        document.getElementById('tutor_1_name').innerHTML = data['data']['tutor_1']['name'];
		        document.getElementById('tutor_2_name').innerHTML = data['data']['tutor_2']['name'];
		        document.getElementById('tutor_1_position').innerHTML = data['data']['tutor_1']['position'];
		        document.getElementById('tutor_2_position').innerHTML = data['data']['tutor_2']['position'];
		        document.getElementById('tutor_1_major').className = 'major ' + data['data']['tutor_1']['color'];
		        document.getElementById('tutor_1_major').innerHTML = data['data']['tutor_1']['major'];
		        document.getElementById('tutor_2_major').className = 'major ' + data['data']['tutor_2']['color'];
		        document.getElementById('tutor_2_major').innerHTML = data['data']['tutor_2']['major'];
		        document.getElementById('tutor_1_email').innerHTML = data['data']['tutor_1']['email'];
			document.getElementById('tutor_2_email').innerHTML = data['data']['tutor_2']['email'];
			var skills_html = '';
		        for(var skill in data['data']['tutor_1']['skills'])
		            skills_html += '<span class="skill">' + data['data']['tutor_1']['skills'][skill] + '</span>'
		        document.getElementById('tutor_1_skills').innerHTML = skills_html;
		        skills_html = '';
		        for(var skill in data['data']['tutor_2']['skills'])
		            skills_html += '<span class="skill">' + data['data']['tutor_1']['skills'][skill] + '</span>'
		        document.getElementById('tutor_2_skills').innerHTML = skills_html;
		    }
		    else {
		        document.getElementById('tutor_1_color').className = 'tutor-color red';
		        document.getElementById('tutor_2_color').className = 'tutor-color red';
		        document.getElementById('tutor_1_img').src = 'assets/img/example_profile.jpg';
		        document.getElementById('tutor_2_img').src = 'assets/img/example_profile.jpg';
		        document.getElementById('tutor_1_name').innerHTML = 'CLOSED';
		        document.getElementById('tutor_2_name').innerHTML = 'CLOSED';
		        document.getElementById('tutor_1_position').innerHTML = 'CLOSED';
		        document.getElementById('tutor_2_position').innerHTML = 'CLOSED';
		        document.getElementById('tutor_1_major').className = 'major red';
		        document.getElementById('tutor_1_major').innerHTML = 'CLOSED';
		        document.getElementById('tutor_2_major').className = 'major red';
		        document.getElementById('tutor_2_major').innerHTML = 'CLOSED';
		    }
		}
	    });
	}
	catch(Exception) {
	    console.log('ERROR: Unable to access server!');
	    success = false;
	}
	if (!success) {
	    document.getElementById('tutor_1_color').className = 'tutor-color red';
	    document.getElementById('tutor_2_color').className = 'tutor-color red';
	    document.getElementById('tutor_1_img').src = 'assets/img/example_profile.jpg';
	    document.getElementById('tutor_2_img').src = 'assets/img/example_profile.jpg';
	    document.getElementById('tutor_1_name').innerHTML = 'ERROR';
	    document.getElementById('tutor_2_name').innerHTML = 'ERROR';
	    document.getElementById('tutor_1_position').innerHTML = 'ERROR';
	    document.getElementById('tutor_2_position').innerHTML = 'ERROR';
	    document.getElementById('tutor_1_major').className = 'major red';
	    document.getElementById('tutor_1_major').innerHTML = 'ERROR';
	    document.getElementById('tutor_2_major').className = 'major red';
	    document.getElementById('tutor_2_major').innerHTML = 'ERROR';
	}
}


// Update everything
updateCalendar();
updateLabStatus();
updateCurrentTutor();
window.setInterval(function(){
    var now = new Date();
    if ((now.getMinutes() == 0 && now.getSeconds() == 0) || (now.getMinutes() == 15 && now.getSeconds() == 0) || (now.getMinutes() == 30 && now.getSeconds() == 0) || (now.getMinutes() == 45 && now.getSeconds() == 0)) {
        updateCalendar();
        updateLabStatus();
        updateCurrentTutor();
    }
}, 1000);
