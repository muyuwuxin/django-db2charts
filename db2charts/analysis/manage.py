# -*- coding: utf-8 -*-
# author: Alfred

from db2charts.analysis.base import AnalysisBase
from db2charts.models import AvailableAnalysisModel
import json

class AnalysisManage(AnalysisBase):

    def __init__(self):
        super(AnalysisManage, self).__init__()

    def get_availables(self):
        availableModels = AvailableAnalysisModel.objects.all()
        models = [{
            'model_name': x.model_name,
            'translated_name': x.translated_name,
            'active': x.active,
            'cols': x.translated_cols
        } for x in availableModels]
        return models

    def get_candidates(self):
        availables = [x['model_name'] for x in self.get_availables()]
        candidates = []
        for db in self.get_dbs():
            models = self.get_models(db)
            for model in models:
                model['active'] = True if model['model_name'] in availables else False
                candidates.append(model)
        return candidates

    def add_available(self, model_name, translated_model_name, cols):
        aam = AvailableAnalysisModel()
        aam.db_name = model_name.split('.')[0]
        aam.model_name = model_name
        aam.translated_name = translated_model_name
        aam.active = True
        aam.translated_cols = cols
        aam.save()

    def update_available(self, model_name, translated_model_name, cols):
        aam = AvailableAnalysisModel.objects.get(model_name=model_name)
        aam.translated_name = translated_model_name
        aam.translated_cols = cols
        aam.save()

    def delete_available(self, model_name):
        aam = AvailableAnalysisModel.objects.get(model_name=model_name)
        aam.delete()

    def set_active(self, model_name, active):
        aam = AvailableAnalysisModel.objects.get(model_name=model_name)
        aam.active = active
        aam.save()