query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.traffic_data (
            traffic_id SERIAL PRIMARY KEY,
            road_name TEXT,
            latitude DECIMAL(10, 6),
            longitude DECIMAL(10, 6),
            current_speed INT,
            free_flow_speed INT,
            current_travel_time INT,
            free_flow_travel_time INT,
            road_closure BOOLEAN DEFAULT FALSE,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            mapurl TEXT,
            traffic_condition VARCHAR(50),
            weather_id UUID REFERENCES {schema_name}.weather_data(weather_id),
            UNIQUE(road_id,recorded_at)
            FOREIGN KEY (road_id) REFERENCES {schema_name}.roads(road_id) ON DELETE CASCADE    
        );
        """
        cursor.execute(query=query) 
        conn.commit()
        logger.info(f"Table 'traffic_data' is ready.", extra={"stage": "table_setup"})
        # Create index for traffic_data table safely
        try:
            cursor.execute(f"""
                        DO $$ 
                            BEGIN
                                IF NOT EXISTS (
                                    SELECT 1 FROM pg_indexes WHERE LOWER(indexname) = LOWER('traffic_Data_road_id_idx')
                                ) THEN
                                    CREATE INDEX traffic_Data_road_id_idx ON roads_traffic.traffic_data(road_id);
                                END IF;
                            END $$;

                    """)
            conn.commit()
            logger.info("Index 'traffic_Data_road_id_idx' created successfully.", extra={"stage": "index_creation"})
        except Exception as e:
            conn.rollback()
            logger.warning(f"Skipping index creation for 'traffic_Data_road_id_idx': {e}",
                           extra={"stage": "index_creation"})

        query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.weather_data (
            weather_id UUID PRIMARY KEY DEFAULT get_random_uuid(),
            latitude DECIMAL(10, 6),
            longitude DECIMAL(10, 6),
            weather_conditions VARCHAR(50) ,
            temperature FLOAT,
            humidity FLOAT,
            recorded_at TIMESTAMP NOT NULL,
            UNIQUE(latitude,longitude,recorded_at)       
        );
        """
        cursor.execute(query=query) 
        conn.commit()
        logger.info(f"Table 'weather_data' is ready.", extra={"stage": "table_setup"})
        # Create index for traffic_data table safely
        try:
            cursor.execute(f"""
                        DO $$ 
                            BEGIN
                                IF NOT EXISTS (
                                    SELECT 1 FROM pg_indexes WHERE LOWER(indexname) = LOWER('traffic_Data_road_id_idx')
                                ) THEN
                                    CREATE INDEX traffic_Data_road_id_idx ON roads_traffic.traffic_data(road_id);
                                END IF;
                            END $$;

                    """)
            conn.commit()
            logger.info("Index 'traffic_Data_road_id_idx' created successfully.", extra={"stage": "index_creation"})
        except Exception as e:
            conn.rollback()
            logger.warning(f"Skipping index creation for 'traffic_Data_road_id_idx': {e}",
                           extra={"stage": "index_creation"})

        logger.info("Database setup completed successfully.", extra={"stage": "success"})
