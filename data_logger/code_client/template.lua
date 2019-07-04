sda, scl = 2, 1
i2c.setup(0, sda, scl, i2c.SLOW) -- call i2c.setup() only once

sensors = {
    {% for sensor_name in data -%} 
    {
        name = "{{ sensor_name }}",
        init = {{ data[sensor_name].init }},
        read = {{ data[sensor_name].read }},
        value = {
            {%- for v in data[sensor_name].value -%}
            "{{v}}", 
            {%- endfor -%}
        },
        records = {
            {%- for v in data[sensor_name].records -%}
            {{"true" if v else "false"}}, 
            {%- endfor -%}
        }
    },
    {%- endfor %}
}

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