import { Component, OnInit, QueryList, ViewChild, ViewChildren, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Model } from './model';
import { ModelStorageService } from '../model-storage.service';
import { ModelOrchestrationService } from '../model-orchestration.service';
import { MessageService } from 'primeng/api';
import { FileUpload } from 'primeng/fileupload';


@Component({
  selector: 'app-model-management',
  templateUrl: './model-management.component.html',
  styleUrls: ['./model-management.component.css'],
  providers: [MessageService]
})
export class ModelManagementComponent implements OnInit, AfterViewInit {

  @ViewChildren("fp") fileUploadQuery: QueryList<FileUpload>;

  fileUpload: FileUpload;

  modelName = '';
  uploadProgress = 0;
  fileName = '';
  models: Model[];
  displayDialog = false;
  showNameError = false;
  showFileError = false;

  constructor(private http: HttpClient, private modelStorageService: ModelStorageService,
    private modelOrchestrationService: ModelOrchestrationService, private msgService: MessageService) {
      this.models = [];
  }

  ngOnInit(): void {
    this.updateModelList();
  }

  ngAfterViewInit(): void {
    this.fileUploadQuery.changes.subscribe((fileUploads: QueryList <FileUpload>) => {
      if(fileUploads.first) {
        this.fileUpload = fileUploads.first;
        this.fileUpload.onError.subscribe((data: any) => {
          this.updateModelList();
          this.msgService.add({severity: "error", summary: `Failed to upload model.`, detail: ""});
        });
        this.fileUpload.onUpload.subscribe((data: any) => {
          this.updateModelList();
          this.msgService.add({severity: "success", summary: `New model has been uploaded.`, detail: ""});
        });
      }
    });
  }

  upload(event: any) {
    this.showNameError = false;
    this.showFileError = false;
    if(this.modelName === '') {
      this.showNameError = true;
      return;
    }
    if(this.fileUpload.files.length == 0) {
      this.showFileError = true;
      return;
    }
    this.fileUpload.upload();
  }

  onBeforeUpload(event: any) {
    event.formData.append("name", this.modelName);
  }

  onProgress(event: any) {
    this.uploadProgress = event.progress;
    if(this.uploadProgress >= 100) {
      this.displayDialog = false;
    }
  }

  onError(event: any) {
    console.log("on error");
  }

  deleteModel(selectedModel: Model) {
    this.modelStorageService.deleteModel(selectedModel.id).subscribe(
      (data: any) => {
        this.models = this.models.filter(model => model.id != selectedModel.id)
        this.msgService.add({severity: "success", summary: `${selectedModel.id} has been deleted.`, detail: ""});
      },
      (error) => {
        console.log(error);
        this.msgService.add({severity: "error", summary: `Unable to delete model.`, detail: ""});
      },
      () => {
        console.log("Completed");
      }
    );
  }

  activateModel(selectedModel: Model) {
    this.modelOrchestrationService.activateModel(selectedModel.id).subscribe((data: any) => {
      selectedModel.active = true;
      this.msgService.add({severity: "success", summary: `${selectedModel.id} has been activated.`, detail: ""});
    },
    (error) => {
      console.log(error);
      this.msgService.add({severity: "error", summary: `Unable to activate model.`, detail: ""});
    },
    () => {
      console.log("Completed");
    });
  }

  deactivateModel(selectedModel: Model) {
    this.modelOrchestrationService.deactivateModel(selectedModel.id).subscribe((data: any) => {
      selectedModel.active = false;
      this.msgService.add({severity: "success", summary: `${selectedModel.id} has been deactivated.`, detail: ""});
    },
    (error) => {
      console.log(error);
      this.msgService.add({severity: "error", summary: `Unable to deactivate model.`, detail: ""});
    },
    () => {
      console.log("Completed");
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
    this.showNameError = false;
    this.showFileError = false;
    this.displayDialog = true;
    this.modelName = "";
    this.uploadProgress = 0;
  }
}
