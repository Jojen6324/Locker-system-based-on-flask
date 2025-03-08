from models.database import execute_query

class LocationModel:
    def __init__(self, config):
        self.config = config
    
    def get_all_locations(self):
        sql = "SELECT * FROM locations"
        return execute_query(self.config, sql, ())
    
    def get_location_by_id(self, location_id):
        sql = "SELECT * FROM locations WHERE id = %s"
        val = (location_id,)
        result = execute_query(self.config, sql, val)
        return result[0] if result else None