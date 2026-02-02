from sqlalchemy import text
from data.db.db_config import engine

def register_feature_view( feature_view: str, description: str ):
    sql =    """

        INSERT INTO feature_view_registry 
        ( feature_view, description )
        VALUES 
        ( :feature_view, :description )
        ON CONFLICT 
        ( feature_view ) 
        DO NOTHING;

        """
    with engine.begin() as conn:
        conn.execute(text(sql), { "feature_view": feature_view, "description": description })

def registry_feature(
        feature_name: str,
        feature_view: str,
        description: str,
        data_type: str,
        source_column: str,
        transformation: str,
    ):
    sql = """

        INSERT INTO feature_registry 
        ( feature_name, feature_view, description, data_type, source_column, transformation )
        VALUES 
        ( :feature_name, :feature_view, :description, :data_type, :source_column, :transformation )
        ON CONFLICT 
        ( feature_name, feature_view ) 
        DO NOTHING;

        """
    
    with engine.begin() as conn:
        conn.execute(text(sql),
                     { "feature_name": feature_name, 
                      "feature_view": feature_view, 
                      "description": description, 
                      "data_type": data_type,
                      "source_column": source_column,
                      "transformation": transformation
                     },
                    )