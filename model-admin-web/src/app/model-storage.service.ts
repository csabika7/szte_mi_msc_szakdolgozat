import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ModelStorageService {

  constructor(private httpClient: HttpClient) { }

  deleteModel(model_id: string) {
    return this.httpClient.delete(`/v1/model-store/model/${model_id}`);
  }
}
