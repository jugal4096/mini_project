import sqlite3

def init_db():
    conn = sqlite3.connect("trains.db")
    cur = conn.cursor()

    # Reset table
    cur.execute("DROP TABLE IF EXISTS trains")

    # Schema
    cur.execute("""
    CREATE TABLE trains (
        train_no TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        source TEXT,
        destination TEXT,
        dep_time TEXT,
        arr_time TEXT,
        duration TEXT,
        avg_speed INTEGER,

        runs_sun INTEGER,
        runs_mon INTEGER,
        runs_tue INTEGER,
        runs_wed INTEGER,
        runs_thu INTEGER,
        runs_fri INTEGER,
        runs_sat INTEGER,

        direction TEXT
    )
    """)

    # Day parser
    def parse_days(days_str):
        d = days_str.split()
        return {
            "sun": int(d[0] == "S"),
            "mon": int(d[1] == "M"),
            "tue": int(d[2] == "T"),
            "wed": int(d[3] == "W"),
            "thu": int(d[4] == "T"),
            "fri": int(d[5] == "F"),
            "sat": int(d[6] == "S"),
        }

    # ------------------------------
    # ALL TRAINS (UNCHANGED DATA)
    # ------------------------------
    trains = [
        # OLD DATA (no direction → will default DOWN)
        ("17020","Hyderabad - Hisar Weekly Express","EXP","CPSN","??","00:05","01:15","1h10m",54,"S M T W T F S"),
        ("17611","Rajya Rani Express","EXP","CPSN","??","01:35","02:50","1h15m",50,"S M T W T F S"),
        ("17208","Machilipatnam - Shirdi Weekly","EXP","CPSN","??","03:32","04:25","0h53m",71,"S M T W T F S"),
        ("17206","Kakinada Port - Shirdi Express","EXP","CPSN","??","03:32","04:25","0h53m",71,"S M T W T F S"),
        ("17002","Secunderabad - Shirdi Express","EXP","CPSN","??","03:32","04:25","0h53m",71,"S M T W T F S"),
        ("12787","Narasapur - Nagarsol SF","SF","CPSN","??","03:55","04:50","0h55m",68,"S M T W T F S"),
        ("17064","Ajanta Express","EXP","CPSN","??","04:02","05:25","1h23m",45,"S M T W T F S"),
        ("18503","Visakhapatnam - Shirdi Weekly","EXP","CPSN","??","05:00","06:15","1h15m",50,"S M T W T F S"),
        ("17417","Tirupati - Shirdi Weekly (Raichur)","EXP","CPSN","??","05:00","06:15","1h15m",50,"S M T W T F S"),
        ("17425","Tirupati - Shirdi Weekly (Guntur)","EXP","CPSN","??","05:00","06:15","1h15m",50,"S M T W T F S"),
        ("77621","Jalna - Nagarsol DEMU","DEMU","CPSN","??","05:50","07:08","1h18m",48,"S M T W T F S"),
        ("11410","Nizamabad - Pune Express","EXP","CPSN","??","06:30","08:25","1h55m",33,"S M T W T F S"),
        ("17231","Narasapur - Nagarsol Express","EXP","CPSN","??","06:30","07:45","1h15m",50,"S M T W T F S"),
        ("20705","Vande Bharat Express","VB","CPSN","??","07:35","08:23","0h48m",78,"S M T W T F S"),
        ("12072","Jan Shatabdi Express","JSHTB","CPSN","??","08:25","09:35","1h10m",54,"S M T W T F S"),
        ("17688","Marathwada Express","EXP","CPSN","??","08:50","09:50","1h00m",63,"S M T W T F S"),
        ("16733","Rameswaram - Okha Weekly","EXP","CPSN","??","09:00","10:05","1h05m",58,"S M T W T F S"),
        ("16003","Chennai - Nagarsol Weekly","EXP","CPSN","??","09:00","10:05","1h05m",58,"S M T W T F S"),
        ("01012","Hyderabad - Mumbai CSMT Summer Special","EXP","J","CPSN","09:02","10:10","1h08m",55,"S M T W T F S"),

("07621","Nanded - Hazrat Nizamuddin Special","EXP","J","CPSN","11:20","12:55","1h35m",40,"S M T W T F S"),

("12753","Marathwada Sampark Kranti Express","SKR","J","CPSN","11:20","12:55","1h35m",40,"S M T W T F S"),

("17253","Guntur - Sambhajinagar Express","EXP","J","CPSN","11:50","13:20","1h30m",42,"S M T W T F S"),

("12715","Sachkhand Express","SF","J","CPSN","12:25","13:25","1h00m",63,"S M T W T F S"),

("17618","Tapovan Express","EXP","J","CPSN","13:10","14:30","1h20m",47,"S M T W T F S"),

("17620","Nanded - Sambhajinagar Weekly","EXP","J","CPSN","15:05","16:50","1h45m",36,"S M T W T F S"),

("14621","Nanded - Firozpur Weekly","EXP","J","CPSN","15:05","16:25","1h20m",47,"S M T W T F S"),

("17661","Kacheguda - Nagarsol Express","EXP","J","CPSN","16:50","18:15","1h25m",44,"S M T W T F S"),

("17630","Nanded - Hadapsar Express","EXP","J","CPSN","19:00","20:20","1h20m",47,"S M T W T F S"),

("11002","Nandigram Express","EXP","J","CPSN","20:10","21:25","1h15m",50,"S M T W T F S"),

("17622","Tirupati - Sambhajinagar Weekly","EXP","J","CPSN","20:55","22:40","1h45m",36,"S M T W T F S"),

("17058","Devagiri Express","EXP","J","CPSN","22:15","23:20","1h05m",58,"S M T W T F S"),

("57651","Nanded - Manmad Passenger","PASS","J","CPSN","23:45","01:50","2h05m",30,"S M T W T F S")

        # NEW + UP DATA (WITH direction)
        ("11409","Daund - Nizamabad Express","EXP","CPSN","JALNA","01:10","02:13","1h03m",60,"S M T W T F S","UP"),
        ("17612","Mumbai - Nanded Rajya Rani","EXP","CPSN","JALNA","01:50","03:08","1h18m",48,"S M T W T F S","UP"),
        ("17057","Devagiri Express","EXP","CPSN","JALNA","04:20","05:13","0h53m",71,"S M T W T F S","UP"),
        ("17629","Hadapsar - Nanded Express","EXP","CPSN","JALNA","05:10","06:08","0h58m",65,"S M T W T F S","UP"),
        ("17662","Nagarsol - Kacheguda Express","EXP","CPSN","JALNA","07:20","08:38","1h18m",48,"S M T W T F S","UP"),
        ("16734","Okha - Rameswaram Express","EXP","CPSN","JALNA","07:45","08:48","1h03m",60,"S M T W T F S","UP"),
        ("01011","Mumbai - Hyderabad Special","EXP","CPSN","JALNA","07:45","08:48","1h03m",60,"S M T W T F S","UP"),
        ("57652","Manmad - Nanded Passenger","PASS","CPSN","JALNA","08:45","10:18","1h33m",40,"S M T W T F S","UP"),
        ("12716","Sachkhand Express","SF","CPSN","JALNA","10:05","10:55","0h50m",75,"S M T W T F S","UP"),
        ("17617","Tapovan Express","EXP","CPSN","JALNA","13:10","14:15","1h05m",58,"S M T W T F S","UP"),
        ("12788","Nagarsol - Narasapur SF","SF","CPSN","JALNA","14:05","15:03","0h58m",65,"S M T W T F S","UP"),
        ("17232","Nagarsol - Narasapur Express","EXP","CPSN","JALNA","14:05","15:03","0h58m",65,"S M T W T F S","UP"),
        ("16004","Nagarsol - Chennai Weekly","EXP","CPSN","JALNA","14:50","15:58","1h08m",55,"S M T W T F S","UP"),
        ("17254","Sambhajinagar - Guntur Express","EXP","CPSN","JALNA","16:15","17:00","0h45m",84,"S M T W T F S","UP"),
        ("17687","Marathwada Express","EXP","CPSN","JALNA","17:50","18:40","0h50m",75,"S M T W T F S","UP"),
        ("12071", "Mumbai - Hingoli Jan Shatabdi", "JSHTB", "CPSN", "JALNA", "18:30", "19:25", "0h55m", 68, "S M T W T F S", "UP"),

("20706", "Mumbai - Nanded Vande Bharat", "VB", "CPSN", "JALNA", "18:45", "19:38", "0h53m", 71, "S M T W T F S", "UP"),

("07622", "Nizamuddin - Nanded Special", "EXP", "CPSN", "JALNA", "19:00", "19:53", "0h53m", 71, "S M T W T F S", "UP"),

("17019", "Hisar - Hyderabad Weekly", "EXP", "CPSN", "JALNA", "19:20", "20:33", "1h13m", 52, "S M T W T F S", "UP"),

("12754", "Marathwada Sampark Kranti", "SKR", "CPSN", "JALNA", "19:20", "20:33", "1h13m", 52, "S M T W T F S", "UP"),

# DEMU → keep only ONE (remove duplicate 77622)
("77620", "Nagarsol - Jalna DEMU", "DEMU", "CPSN", "JALNA", "19:55", "21:40", "1h45m", 36, "S M T W T F S", "UP"),

("17207", "Shirdi - Machilipatnam Weekly", "EXP", "CPSN", "JALNA", "20:50", "21:43", "0h53m", 71, "S M T W T F S", "UP"),

("17205", "Shirdi - Kakinada Express", "EXP", "CPSN", "JALNA", "20:50", "21:43", "0h53m", 71, "S M T W T F S", "UP"),

("17001", "Shirdi - Secunderabad Express", "EXP", "CPSN", "JALNA", "20:50", "21:43", "0h53m", 71, "S M T W T F S", "UP"),

("17621", "Sambhajinagar - Tirupati Weekly", "EXP", "CPSN", "JALNA", "20:50", "21:43", "0h53m", 71, "S M T W T F S", "UP"),

("14622", "Firozpur - Nanded Weekly", "EXP", "CPSN", "JALNA", "21:00", "22:03", "1h03m", 60, "S M T W T F S", "UP"),

("17063", "Ajanta Express", "EXP", "CPSN", "JALNA", "22:45", "23:45", "1h00m", 63, "S M T W T F S", "UP"),

("18504", "Shirdi - Visakhapatnam Weekly", "EXP", "CPSN", "JALNA", "23:15", "00:08", "0h53m", 71, "S M T W T F S", "UP"),

("17418", "Shirdi - Tirupati (Raichur)", "EXP", "CPSN", "JALNA", "23:15", "00:08", "0h53m", 71, "S M T W T F S", "UP"),

("17426", "Shirdi - Tirupati (Guntur)", "EXP", "CPSN", "JALNA", "23:15", "00:08", "0h53m", 71, "S M T W T F S", "UP"),

("17619", "Sambhajinagar - Nanded Weekly", "EXP", "CPSN", "JALNA", "23:30", "00:08", "0h38m", 99, "S M T W T F S", "UP"),

("11001", "Nandigram Express", "EXP", "CPSN", "JALNA", "23:45", "00:48", "1h03m", 60, "S M T W T F S", "UP"),
    ]

    # ------------------------------
    # INSERT
    # ------------------------------
    for t in trains:

        # detect direction
        if len(t) == 11:
            direction = t[10]
        else:
            direction = "DOWN"

        days = parse_days(t[9])

        cur.execute("""
        INSERT INTO trains VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            t[0], t[1], t[2], t[3], t[4],
            t[5], t[6], t[7], t[8],
            days["sun"], days["mon"], days["tue"],
            days["wed"], days["thu"], days["fri"], days["sat"],
            direction
        ))

    conn.commit()
    conn.close()

    print("✅ Database initialized correctly")


if __name__ == "__main__":
    init_db()