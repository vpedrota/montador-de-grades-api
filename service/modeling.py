import pandas as pd

class Modeling():

    def __init__(self):
        colnames=['NOME', "DIA", "TURMA/PROFESSOR", "HORARIO"]
        self.ucs = pd.DataFrame(pd.read_csv("database/ucs.csv", encoding="utf-8", sep=";", names=colnames, header=None))
        self.prof = pd.DataFrame(pd.read_csv("database/prof.csv", sep=","))

        self.ucs = self.ucs[self.ucs["NOME"] != " "]

        self.ucs.loc[~self.ucs["TURMA/PROFESSOR"].str.contains("-"), "TURMA/PROFESSOR"] = "0-" + self.ucs.loc[~self.ucs["TURMA/PROFESSOR"].str.contains("-"), "TURMA/PROFESSOR"].astype(str)
        self.ucs["TURMA/PROFESSOR"] = self.ucs["TURMA/PROFESSOR"].str.replace(" - ", "-").str.split("-")
        self.ucs["TURMA"] = self.ucs["TURMA/PROFESSOR"].str[0].str.strip()

        self.ucs["PROFESSORES"] = self.ucs["TURMA/PROFESSOR"].str[1].str.replace(" / ", "/").str.strip()

        self.ucs["HORARIO"] = self.ucs["HORARIO"].str.replace(" - ", "-").str.strip()
        self.ucs.loc[self.ucs["HORARIO"].str.contains("8h00-10h00"), "HORARIO"] = "0" + self.ucs.loc[self.ucs["HORARIO"].str.contains("8h00-10h00"), "HORARIO"].astype(str)
        self.ucs.loc[self.ucs["DIA"].str.contains("Segunda"), "DIA"] = self.ucs.loc[self.ucs["DIA"].str.contains("Segunda"), "DIA"].str.replace(" feira", "")

        self.ucs.drop(["TURMA/PROFESSOR"], axis=1, inplace=True)

        gp_ucs = self.ucs.groupby(["NOME", "TURMA", "PROFESSORES"], as_index=False)["DIA"].count()
        gp_ucs = gp_ucs.sort_values(by=["NOME"]).reset_index()
        gp_ucs = gp_ucs.drop("DIA", axis=1)
        gp_ucs["ID"] = gp_ucs.index

        self.ucs = self.ucs.merge(gp_ucs, on=["NOME", "TURMA", "PROFESSORES"], how="outer")
        self.ucs = self.ucs[["ID", "NOME", "TURMA", "PROFESSORES", "DIA", "HORARIO"]]

    def _df_to_dict(df):
        return df.to_dict("records")

    def _group_by(df):
        return df.groupby(["ID", "NOME", "TURMA", "PROFESSORES"], as_index=False).\
        agg({"DIA":lambda x: list(x), "HORARIO":lambda x: list(x)})

    def prof_analizer(self, data):

        prof_list = list(self.ucs.loc[self.ucs["ID"].isin(data), "PROFESSORES"].unique())
        prof_list = [prof_list[0].upper()]
        
        if "/" in prof_list[0]:
            prof_list = prof_list[0].split("/")

        if len(prof_list) > 1: 
            filter_data = self.prof[(self.prof["DOCENTE RESPONSAVEL"].str.contains(prof_list[0])) &
                        (self.prof["DOCENTE RESPONSAVEL"].str.contains(prof_list[1]))]

        else: filter_data = self.prof[self.prof["DOCENTE RESPONSAVEL"].str.contains(prof_list[0])]
        
        group_data = filter_data.groupby("DOCENTE RESPONSAVEL", as_index=False).\
                                agg({"NOME DA UC": lambda x: list(x), "APROVADOS" : lambda x: list(x), 
                                    "REPROVADOS": lambda x: list(x), "TOTAL": lambda x: list(x)})
        
        return Modeling._df_to_dict(group_data)

    def get_ucs(self):
        return Modeling._df_to_dict(Modeling._group_by(self.ucs))

    def uc_analizer(self, data):
        data = self.ucs.loc[self.ucs["ID"].isin(data), "NOME"].unique()
        sub_ucs = self.ucs.loc[self.ucs["NOME"].str.contains(data[0]), ["DIA", "HORARIO"]]
        sub_ucs = self.ucs.merge(sub_ucs, how='outer', indicator=True)
        
        list_result = sub_ucs.loc[sub_ucs["_merge"] == "both", "ID"].unique()
        pre_result = self.ucs[~self.ucs["ID"].isin(list_result)]

        return Modeling._df_to_dict(Modeling._group_by(pre_result))