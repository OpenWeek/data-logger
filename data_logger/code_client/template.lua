BROKER_IP = "10.0.3.1"
BROKER_PORT = 1883
SSID = "ow-rpi1"
PWD = "test_passphrase"

MAX_MEASURES_PER_SENSOR = 80 -- as soon there is one sensor with more than the quantity of measures everything measures are send
MIN_MEASURES_PER_SENSOR = 2

LOOP = true

sda, scl = 2, 1
i2c.setup(0, sda, scl, i2c.SLOW) -- call i2c.setup() only once

json = require "json"

sensors = {
    {% for sensor_id in data -%}
    {{ sensor_id }} = {
        type = "{{ data[sensor_id]["type"]}}",
        period = {{ data[sensor_id]["period"]}},
        init = {{ data[sensor_id].init }},
        read = {{ data[sensor_id].read }},
        value = {
            {%- for v in data[sensor_id].value -%}
            "{{v}}",
            {%- endfor -%}
        },
        records = {
            {%- for v in data[sensor_id].records -%}
            {{"true" if v else "false"}},
            {%- endfor -%}
        }
    },
    {%- endfor %}
}

CLIENT_ID = "{{client_id}}"


function write_json(file_name, d)
	file.open(file_name, "w")
	file.writeline(json.stringify(d))
	file.close()
end

function load_json(file_name)
	file.open(file_name)
	f = file.read()
	file.close()
	return json.parse(f)
end

function load_memory()
	t = load_json("time.json")
	m = load_json("measures.json")
	return t, m
end

time, measures = load_memory()

function add_measures(sensor_name, value)
	-- if measures[sensor_name] == nil then
	-- 	measures[sensor_name] = {}
	-- end
	table.insert(measures[sensor_name], value)
end


function time_to_measure(sensor_id)
	if time[sensor_id] >= sensors[sensor_id].period then
		time[sensor_id] = 0
		return true
	else
		return false
	end
end

function time_to_send()
	cnt_measures_done_now = 0 -- during this run
	cnt_measures_done_min = -1 -- per sensor_id
	cnt_measures_done_max = -1 -- per sensor_id

	for sensor_id, _ in pairs(time) do
		if time[sensor_id] == 0 then 
			cnt_measures_done_now = cnt_measures_done_now + 1 
		end
		
		nb_measures = #measures[sensor_id]
		if cnt_measures_done_min == -1 or cnt_measures_done_min > nb_measures then
			cnt_measures_done_min = nb_measures
		end
		if cnt_measures_done_max == -1 or cnt_measures_done_max < nb_measures then
			cnt_measures_done_max = nb_measures
		end

	end

	return cnt_measures_done_max >= MAX_MEASURES_PER_SENSOR or cnt_measures_done_min >= MIN_MEASURES_PER_SENSOR
end


for sensor_id, sensor in pairs(sensors) do
	print("*init " .. sensor_id)
	sensor.init()
	r = {sensor.read()}

	if time_to_measure(sensor_id) then
		sensor_measures = {}
		for i = 1, #sensor.value do
			if sensor.records[i] then
				sensor_measures[sensor.value[i]] = r[i] 
				print(sensor.value[i] .. " - " ..r[i])
			end
		end
		add_measures(sensor_id, sensor_measures)
	end
end

function process(client, measures)

	client:publish("/" .. CLIENT_ID, json.stringify(measures), 0, 0,
		function(client) 
			print("MQTT :: sent data")
			save_and_sleep(true)
		end
	)
end

function after_connect(T)
	print("WIFI :: got ip " .. T.IP)
	m = mqtt.Client(CLIENT_ID, 120)
	m:connect(BROKER_IP, BROKER_PORT, 0,
		function(client)
			print("MQTT :: connected")
			process(client, measures)
		end,
		function(client, reason)
			print("MQTT :: connection failed: " .. reason)
		end
	)
end

function connect()
	print("begin connection")
	wifi.eventmon.register(wifi.eventmon.STA_GOT_IP, after_connect)
	wifi.setmode(wifi.STATION)
	wifi.sta.config({ssid = SSID, pwd = PWD, save = false})
end

function empty_measures()
	measures = {}
	for sensor_id, _ in pairs(time) do
		measures[sensor_id] = {}
	end
	return measures
end

function save(sended)
	write_json("time.json", time)

	if sended then measures = empty_measures() end
	write_json("measures.json", measures)
end


function increment_time(sleep_duration)
	for sensor_id, _ in pairs(time) do
		time[sensor_id] = time[sensor_id] + sleep_duration
	end
end

function compute_sleep_duration()
	min_delta = -1

	for sensor_id, _ in pairs(time) do
		delta = sensors[sensor_id].period - time[sensor_id]
		if min_delta == -1 or delta < min_delta then
			min_delta = delta
		end
	end

	if min_delta < 1 then
		return 1
	else
		return min_delta
	end
end

function save_and_sleep(sended)
	sleep_duration = compute_sleep_duration()
	increment_time(sleep_duration)
	save(sended)
	if LOOP then node.dsleep(sleep_duration*1000*1000) end
end

function send()
	if time_to_send() then
		connect()
	else
		save_and_sleep(false)
	end
end

send()