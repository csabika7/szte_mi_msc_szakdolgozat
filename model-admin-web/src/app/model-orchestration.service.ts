import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ModelOrchestrationService {

  constructor(private httpClient: HttpClient) { }


  activateModel(modelId: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };
    return this.httpClient.post(`/v1/model-orchestrator/model/activate/${modelId}`, httpOptions);
  }

  deactivateModel(modelId: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };
    return this.httpClient.post(`/v1/model-orchestrator/model/deactivate/${modelId}`, httpOptions);
  }

  listModels() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };
    return this.httpClient.get('/v1/model-orchestrator/model/list', httpOptions);
  }
}
