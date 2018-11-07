import sqlite3

from config import RULES_DATABASE_PATH


class DbInteractor():
    def __init__(self):
        self._db_file_path = RULES_DATABASE_PATH

    def get_local_preprocessor_list_from_sql(self, domain):
        with sqlite3.connect(self._db_file_path) as sqlite_conn:
            preprocessor_list = sqlite_conn.execute((
                "SELECT P.PreprocessorName "
                "FROM DomainPreprocessorMapping AS DPM "
                "INNER JOIN Preprocessor AS P ON DPM.PreprocessorId=P.PreprocessorId "
                "INNER JOIN Domain AS D ON D.DomainId=DPM.DomainId "
                "WHERE D.DomainName=\"{0}\"").format(domain))
        return [preprocessor_tuple[0] for preprocessor_tuple in preprocessor_list]

    def get_domain_list_from_sql(self):
        with sqlite3.connect(self._db_file_path) as sqlite_conn:
            domains = sqlite_conn.execute("""SELECT DomainName FROM Domain""")
        return [domain[0] for domain in domains]

    def get_intent_list_from_db(self):
        with sqlite3.connect(self._db_file_path) as sqlite_conn:
            intent_list = sqlite_conn.execute((
                "SELECT I.IntentId, D.DomainName I,InitialStateId "
                "FROM DomainIntentMapping AS DIM "
                "INNER JOIN Domain  AS D "
                "ON DIM.DomainId=D.DomainId "
                "INNER JOIN Intent  AS I "
                "ON DIM.IntentId=I.IntentId")).fetchall()
            intent_parameter_list = sqlite_conn.execute((
                "SELECT K.Name, IP.IntentId, IP.Name, IP.Ask, IP.MaxNum, IP.ReAsk, IP.DefaultValue, IP.DataType "
                "FROM IntentParameter AS IP "
                "INNER JOIN Keyword AS K "
                "ON IP.KeywordId=K.KeywordId")).fetchall()
            intent_reply_list = sqlite_conn.execute((
                "SELECT IntentId, StateId, Reply, LastStateId "
                "FROM IntentReply")).fetchall()
        return intent_list, intent_parameter_list, intent_reply_list

    def get_keywords_dic(self, domain):
        with sqlite3.connect(self._db_file_path) as sqlite_conn:
            keyword_data = sqlite_conn.execute((
                "SELECT K.Name, K.Re "
                "FROM Keyword AS K "
                "INNER JOIN DomainKeywordMapping AS DK ON DK.KeywordId=K.KeywordId "
                "INNER JOIN Domain AS D ON DK.DomainId=D.DomainId "
                "WHERE D.DomainName=\"{0}\"").format(domain))
        return dict(keyword_data)

    def get_intent_replacer_dic(self):
        with sqlite3.connect(self._db_file_path) as sqlite_conn:
            intent_replacer_data = sqlite_conn.execute((
                "SELECT Name, Re "
                "FROM IntentReMappingReplacer"))
        return dict(intent_replacer_data)

    def get_re_intentId_mapping(self, domain):
        with sqlite3.connect(self._db_file_path) as sqlite_conn:
            re_intent_id_mapping_list = sqlite_conn.execute((
                "SELECT IRM.IntentReMappingId, IRM.Re, I.IntentId, IRM.FromStateId, IRM.ToStateId "
                "FROM IntentReMapping AS IRM "
                "INNER JOIN Intent AS I "
                "ON IRM.IntentId=I.IntentId "
                "INNER JOIN DomainIntentMapping AS DIM "
                "ON DIM.IntentId=I.IntentId "
                "INNER JOIN Domain AS D "
                "ON DIM.DomainId=D.DomainId "
                "WHERE D.DomainName=\"{0}\" "
                "ORDER BY IRM.Priority DESC").format(domain)).fetchall()
        return re_intent_id_mapping_list
