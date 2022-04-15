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

  modelName = '';
  uploadProgress = 0;
  fileName = '';
  models: Model[];
  displayDialog = false;

  constructor(private http: HttpClient, private modelStorageService: ModelStorageService,
    private modelOrchestrationService: ModelOrchestrationService) {
      this.models = [];
  }

  ngOnInit(): void {
    this.updateModelList();
  }

  onBeforeUpload(event: any) {
    event.formData.append("name", this.modelName);
  }

  onProgress(event: any) {
    this.uploadProgress = event.progress;
    if(this.uploadProgress >= 100) {
      this.displayDialog = false;
      // workaround unUpload does not work
      this.updateModelList();
    }
  }

  deleteModel(selectedModel: Model) {
    this.modelStorageService.deleteModel(selectedModel.id).subscribe((data: any) => {
      this.models = this.models.filter(model => model.id != selectedModel.id)
    });
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

  getEventValue($event:any) :string {
    return $event.target.value;
  }

  showCreateDialog() {
    this.displayDialog = true;
    this.modelName = "";
    this.uploadProgress = 0;
  }
}
