from typing import Generator

from neo4j import GraphDatabase

from core.config import settings

class Neo4jDB:
    def __init__(self, uri: str, user: str, password: str):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    def connect(self):
        """Tạo kết nối đến Neo4j"""
        if not self._driver:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        return self._driver

    def close(self):
        """Đóng kết nối"""
        if self._driver:
            self._driver.close()

    def create_nodes_and_edges(self):
        """Tạo cấu trúc node và edge mà không có dữ liệu"""
        with self.connect() as session:
            # Tạo các kiểu node
            session.run("CREATE (n:Person)")
            session.run("CREATE (n:Book)")
            session.run("CREATE (n:Author)")

            # Tạo các kiểu quan hệ giữa các node
            session.run("""
                MATCH (a:Person), (b:Book)
                CREATE (a)-[:READS]->(b)
            """)
            session.run("""
                MATCH (a:Author), (b:Book)
                CREATE (a)-[:WROTE]->(b)
            """)

    def create_nodes_and_edges(self):
        """Tạo cấu trúc node và edge mà không có dữ liệu"""
        with self.connect() as session:
            # Tạo các kiểu node cho học bổng và các thuộc tính liên quan
            session.run("CREATE (s:Scholarship)")
            session.run("CREATE (m:Major)")
            session.run("CREATE (c:Continent)")
            session.run("CREATE (co:Country)")
            session.run("CREATE (city:City)")
            session.run("CREATE (ec:EducationCriteria)")
            session.run("CREATE (rc:ResearchCriteria)")
            session.run("CREATE (exp:ExperienceCriteria)")
            session.run("CREATE (ac:AchievementCriteria)")
            session.run("CREATE (cert:CertificationCriteria)")
            session.run("CREATE (gender:GenderCriteria)")
            session.run("CREATE (age:AgeCriteria)")
            session.run("CREATE (ethnicity:EthnicityCriteria)")

            # Tạo các quan hệ giữa các node
            session.run("""
                MATCH (s:Scholarship), (m:Major)
                CREATE (s)-[:RELATED_TO]->(m)
            """)
            session.run("""
                MATCH (s:Scholarship), (c:Continent)
                CREATE (s)-[:AVAILABLE_ON]->(c)
            """)
            session.run("""
                MATCH (s:Scholarship), (co:Country)
                CREATE (s)-[:AVAILABLE_IN]->(co)
            """)
            session.run("""
                MATCH (s:Scholarship), (city:City)
                CREATE (s)-[:LOCATED_IN]->(city)
            """)
            session.run("""
                MATCH (s:Scholarship), (ec:EducationCriteria)
                CREATE (s)-[:HAS_CRITERIA]->(ec)
            """)
            session.run("""
                MATCH (s:Scholarship), (rc:ResearchCriteria)
                CREATE (s)-[:HAS_CRITERIA]->(rc)
            """)
            session.run("""
                MATCH (s:Scholarship), (exp:ExperienceCriteria)
                CREATE (s)-[:HAS_CRITERIA]->(exp)
            """)
            session.run("""
                MATCH (s:Scholarship), (ac:AchievementCriteria)
                CREATE (s)-[:HAS_CRITERIA]->(ac)
            """)
            session.run("""
                MATCH (s:Scholarship), (cert:CertificationCriteria)
                CREATE (s)-[:HAS_CRITERIA]->(cert)
            """)
            session.run("""
                MATCH (s:Scholarship), (gender:GenderCriteria)
                CREATE (s)-[:HAS_CRITERIA]->(gender)
            """)
            session.run("""
                MATCH (s:Scholarship), (age:AgeCriteria)
                CREATE (s)-[:HAS_CRITERIA]->(age)
            """)
            session.run("""
                MATCH (s:Scholarship), (ethnicity:EthnicityCriteria)
                CREATE (s)-[:HAS_CRITERIA]->(ethnicity)
            """)


neo4j_db = Neo4jDB(
    uri=settings.NEO4J_URI,
    user=settings.NEO4J_USERNAME,
    password=settings.NEO4J_PASSWORD
)


def get_neo4j_session() -> Generator[GraphDatabase, None, None]:
    """Trả về đối tượng session của Neo4j"""
    try:
        driver = neo4j_db.connect()
        yield driver
    finally:
        neo4j_db.close()

neo4j_db.create_nodes_and_edges()