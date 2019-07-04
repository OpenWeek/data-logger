BROKER_IP = "10.0.3.1"
BROKER_PORT = 1883
SSID = "ow-rpi1"
PWD = "test_passphrase"

sda, scl = 2, 1
i2c.setup(0, sda, scl, i2c.SLOW) -- call i2c.setup() only once

json = require "json"

sensors = {
    {% for sensor_id in data -%}
    {
        name = "{{ sensor_id }}",
        type = "{{ data[sensor_id]["type"]}}",
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

measures = {}

function add_measure(sensor_name, measure, value)
	if measures[sensor_name] == nil then
		measures[sensor_name] = {}
	end
	measures[sensor_name][measure] = value
end

for _, sensor in ipairs(sensors) do
	print("*init " .. sensor.name)
	sensor.init()
	r = {sensor.read()}

	for i = 1, #sensor.value do
		if sensor.records[i] then
			add_measure(sensor.name, sensor.value[i], r[i])
			print(sensor.value[i] .. " - " ..r[i])
		end
	end
end

function process(client, measures)
	for sensor_id, values in pairs(measures) do
		client:publish("/" .. sensor_id, json.stringify(values), 0, 0,
			function(client) print("MQTT :: sent data") end
		)
		-- for measure, value in pairs(values) do
		-- 	topic = "/" .. sensor_name .. "/" .. measure
		-- 	client:publish(topic, value, 0, 0,
		-- 		function(client) print("MQTT :: sent data") end
		-- 	)
		-- end
	end
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

wifi.eventmon.register(wifi.eventmon.STA_GOT_IP, after_connect)
wifi.setmode(wifi.STATION)
wifi.sta.config({ssid = SSID, pwd = PWD, save = false})
