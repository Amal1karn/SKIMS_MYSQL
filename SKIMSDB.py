import mysql.connector


def create_flight_db():
    # Establish connection to MySQL
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1223334444@SK"
    )
    cur = con.cursor()

    # Create the 'flight' database if it doesn't exist
    cur.execute("CREATE DATABASE IF NOT EXISTS flight")
    cur.execute("USE flight")

    # Create separate tables for each category if they don't exist
    categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                  "Connectors", "Voltage_n_Regulator", "LEDs",
                  "Diodes_n_Rectifiers", "Others"]

    for category in categories:
        cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS `{category}` (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            date DATE,
                            mfgnum VARCHAR(255) NOT NULL,
                            partnum VARCHAR(255),
                            custPO VARCHAR(255),
                            description TEXT,
                            quantity INT NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        )
                    """)
        cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS `{category}_summary` (
                            mfgnum VARCHAR(255) PRIMARY KEY,
                            total_quantity INT NOT NULL
                        )
                    """)

        # Create the trigger for updating the timestamp
        trigger_name = f"update_{category}_timestamp"
        cur.execute(f"""
                    CREATE TRIGGER IF NOT EXISTS {trigger_name}
                    AFTER UPDATE ON `{category}`
                    FOR EACH ROW
                    BEGIN
                        UPDATE `{category}`
                        SET timestamp = CURRENT_TIMESTAMP
                        WHERE id = OLD.id;
                    END;
                """)

    con.commit()
    con.close()


create_flight_db()


def create_nonflight_db():
    # Establish connection to MySQL
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1223334444@SK"
    )
    cur = con.cursor()

    # Create the 'flight' database if it doesn't exist
    cur.execute("CREATE DATABASE IF NOT EXISTS nonflight")
    cur.execute("USE nonflight")

    # Create separate tables for each category if they don't exist
    categories = ["Resistor", "Capacitor", "Inductor", "HeaderWirehousing",
                  "Connectors", "Voltage_n_Regulator", "LEDs",
                  "Diodes_n_Rectifiers", "Others"]

    for category in categories:
        cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS `{category}` (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            date DATE,
                            mfgnum VARCHAR(255) NOT NULL,
                            partnum VARCHAR(255),
                            custPO VARCHAR(255),
                            description TEXT,
                            quantity INT NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        )
                    """)
        cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS `{category}_summary` (
                            mfgnum VARCHAR(255) PRIMARY KEY,
                            total_quantity INT NOT NULL
                        )
                    """)

        # Create the trigger for updating the timestamp
        trigger_name = f"update_{category}_timestamp"
        cur.execute(f"""
                    CREATE TRIGGER IF NOT EXISTS {trigger_name}
                    AFTER UPDATE ON `{category}`
                    FOR EACH ROW
                    BEGIN
                        UPDATE `{category}`
                        SET timestamp = CURRENT_TIMESTAMP
                        WHERE id = OLD.id;
                    END;
                """)

    con.commit()
    con.close()


create_nonflight_db()


def suppliers_db():
    # Establish a connection to the MySQL server
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1223334444@SK"
    )
    cur = con.cursor()

    # Create the 'suppliers' database if it doesn't exist
    cur.execute("CREATE DATABASE IF NOT EXISTS suppliers")
    cur.execute("USE suppliers")

    # Table for Suppliers
    cur.execute("CREATE TABLE IF NOT EXISTS supplier ("
                "invoice INT PRIMARY KEY,"
                "name VARCHAR(255),"
                "contact VARCHAR(255),"
                "email VARCHAR(255),"
                "description TEXT)")
    con.commit()

    # Table for Login
    cur.execute("CREATE TABLE IF NOT EXISTS login ("
                "username VARCHAR(255) PRIMARY KEY,"
                "password VARCHAR(255),"
                "email VARCHAR(255))")
    con.commit()

    con.close()


suppliers_db()


def serial_tracking():
    # Connect to the MySQL database
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1223334444@SK"
    )
    cur = con.cursor()

    # Create the 'suppliers' database if it doesn't exist
    cur.execute("CREATE DATABASE IF NOT EXISTS serialtracking")
    cur.execute("USE serialtracking")

    # Create separate tables for each if they don't exist
    Subsystems = ["FM_SubsystemTest", "EDM_SubsystemTest"]

    for Subsystem in Subsystems:
        # Create a table to store item details if it doesn't exist
        cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS `{Subsystem}` (
                        Id INT AUTO_INCREMENT PRIMARY KEY,
                        Tested_Date VARCHAR(255),
                        SystemName VARCHAR(255),
                        Subsystem_SN VARCHAR(255),
                        Part_number VARCHAR(255),
                        Revision VARCHAR(255),
                        Tested_By VARCHAR(255),
                        Result VARCHAR(255),
                        Test_Report_Link VARCHAR(255),
                        Comments TEXT,
                        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        con.commit()

        # Create the trigger for updating the timestamp
        trigger_name = f"update_{Subsystem}_timestamp"
        cur.execute(f"""
                    CREATE TRIGGER IF NOT EXISTS {trigger_name}
                    BEFORE UPDATE ON `{Subsystem}`
                    FOR EACH ROW
                    SET NEW.Timestamp = CURRENT_TIMESTAMP;
                """)

    # Create separate tables for each if they don't exist
    Finals = ["FM_SatelliteIntegration", "EDM_SatelliteIntegration"]

    for Final in Finals:
        # Create a table to store item details if it doesn't exist
        cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS `{Final}` (
                        Id INT AUTO_INCREMENT PRIMARY KEY,
                        Tested_Date VARCHAR(255),
                        Satellite_SN VARCHAR(255),
                        SystemName VARCHAR(255),
                        Subsystem_SN VARCHAR(255),
                        Part_number VARCHAR(255),
                        Revision VARCHAR(255),
                        Tested_By VARCHAR(255),
                        Status VARCHAR(255),
                        Test_Report_Link VARCHAR(255),
                        Comments TEXT,
                        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

        # Create the trigger for updating the timestamp
        trigger_name = f"update_{Final}_timestamp"
        cur.execute(f"""
                    CREATE TRIGGER IF NOT EXISTS {trigger_name}
                    BEFORE UPDATE ON `{Final}`
                    FOR EACH ROW
                    SET NEW.Timestamp = CURRENT_TIMESTAMP;
                """)

    con.commit()
    con.close()


serial_tracking()
