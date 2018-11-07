import sqlite3
import config

class SynonymPreprocessor():
    def __init__(self, domain_name=None):
        """[summary]

        Arguments:
            synonym_dic {[dic]} -- {'test':['test1', 'test2']|
        """
        self._synonym_dic = self._load_synonym_dic(domain_name)

    def process(self, input):
        for main_word, symnonyms in self._synonym_dic.items():
            for symnonym in symnonyms:
                if symnonym in input:
                    input = input.replace(symnonym, main_word)
        return input

    def _load_synonym_dic(self, domain_name):
        def formate_to_synonym_dic(synonym_list):
            tmp_synonym_dic = {}
            for word, synonym in synonym_list:
                if word in tmp_synonym_dic:
                    tmp_synonym_dic[word].append(synonym)
                else:
                    tmp_synonym_dic[word] = [synonym]

            return tmp_synonym_dic

        if domain_name:
            synonym_list = self._get_domain_synonym_list(domain_name)
        else:
            synonym_list = self._get_gloabl_synonym_list()

        synonym_dic = formate_to_synonym_dic(synonym_list)
        return synonym_dic

    def _get_domain_synonym_list(self, domain_name):
        with sqlite3.connect(config.RULES_DATABASE_PATH) as sqlite_conn:
            synonym_list = sqlite_conn.execute((
                "SELECT DW.Word, DS.Synonym "
                "FROM DomainWord AS DW "
                "INNER JOIN DomainSynonym  AS DS "
                "ON DW.DomainWordId=DS.DomainWordId "
                "INNER JOIN Domain AS D "
                "ON DW.DomainId=D.DomainId "
                "WHERE D.DomainName=\"{0}\"")
                .format(domain_name)).fetchall()
            return synonym_list

    def _get_gloabl_synonym_list(self):
        with sqlite3.connect(config.RULES_DATABASE_PATH) as sqlite_conn:
            synonym_list = sqlite_conn.execute((
                "SELECT GW.Word, GS.Synonym "
                "FROM GlobalWord AS GW "
                "INNER JOIN GlobalSynonym  AS GS "
                "ON GW.GlobalWordId=GS.GlobalWordId")).fetchall()
            return synonym_list
