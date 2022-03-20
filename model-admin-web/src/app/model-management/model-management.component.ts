import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Model } from './model';
import { ModelStorageService } from '../model-storage.service';
import { ModelOrchestrationService } from '../model-orchestration.service';


@Component({
  selector: 'app-model-management',
  templateUrl: './model-management.component.html',
  styleUrls: ['./model-management.component.css']
})
export class ModelManagementComponent implements OnInit {

  fileName = '';
  models: Array<Model>;

  constructor(private http: HttpClient, private modelStorageService: ModelStorageService,
    private modelOrchestrationService: ModelOrchestrationService) {
    this.models = [];
  }

  ngOnInit(): void {
    this.updateModelList();
  }

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    const files = target.files as FileList;
    const file = files[0]

    if (file) {
        this.fileName = file.name;
        const formData = new FormData();
        formData.append("name", "random");
        formData.append("model_file", file);
        const upload$ = this.http.post("/v1/model-store/model", formData);
        upload$.subscribe();
    }
  }

  deleteModel(selectedModel: Model) {
    this.modelStorageService.deleteModel(selectedModel.id).subscribe((data: any) => {
      let delIdx = -1;
      for(let i = 0; i < this.models.length; i++) {
        let model = this.models[i];
        if (model.id === selectedModel.id) {
          delIdx = i;
          break;
        }
      }
      if (delIdx >= 0) {
        this.models.splice(delIdx);
      }
    })
  }

  activateModel(selectedModel: Model) {
    this.modelOrchestrationService.activateModel(selectedModel.id).subscribe((data: any) => {
      selectedModel.active = true;
    });
  }

  deactivateModel(selectedModel: Model) {
    this.modelOrchestrationService.deactivateModel(selectedModel.id).subscribe((data: any) => {
      selectedModel.active = false;
    });
  }

  updateModelList() {
    this.modelOrchestrationService.listModels().subscribe((data: any) => {
      this.models = data.models;
    });
  }
}
