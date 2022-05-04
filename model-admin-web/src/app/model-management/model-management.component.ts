import { Component, OnInit, OnDestroy, QueryList, ViewChildren, AfterViewInit } from '@angular/core';
import { Model } from './model';
import { ModelOrchestrationService } from '../model-orchestration.service';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { FileUpload } from 'primeng/fileupload';

@Component({
  selector: 'app-model-management',
  templateUrl: './model-management.component.html',
  styleUrls: ['./model-management.component.css'],
  providers: [MessageService]
})
export class ModelManagementComponent implements OnInit, OnDestroy, AfterViewInit {

  @ViewChildren("fp") fileUploadQuery: QueryList<FileUpload>;
  fileUpload: FileUpload;
  modelName = '';
  uploadProgress = 0;
  fileName = '';
  models: Model[];
  displayDialog = false;
  showNameError = false;
  showFileError = false;
  showfileFormatError = false;
  updateAccessTokenJobId: any;

  constructor(private modelOrchestrationService: ModelOrchestrationService, private msgService: MessageService, private httpClient: HttpClient) {
      this.models = [];
  }

  ngOnInit(): void {
    this.updateModelList();
    this.updateAccessTokenJobId = setInterval(() => {
      this.httpClient.get("/status").subscribe((data: any) => {
        // Keeping access token up to date
        console.log("Getting backend status.");
      });
    }, 50000);
  }

  ngOnDestroy(): void {
    clearInterval(this.updateAccessTokenJobId);
  }

  ngAfterViewInit(): void {
    this.fileUploadQuery.changes.subscribe((fileUploads: QueryList <FileUpload>) => {
      if(fileUploads.first) {
        this.fileUpload = fileUploads.first;
        this.fileUpload.onError.subscribe((data: any) => {
          this.msgService.add({severity: "error", summary: `Failed to upload model.`, detail: data.error.error});
        });
        this.fileUpload.onUpload.subscribe((data: any) => {
          this.updateModelList();
          this.msgService.add({severity: "success", summary: `New model has been uploaded.`, detail: ""});
        });
      }
    });
  }

  upload(event: any): void {
    this.showNameError = false;
    this.showFileError = false;
    this.showfileFormatError = false;
    if(this.modelName === '') {
      this.showNameError = true;
      return;
    }
    if(this.fileUpload.files.length == 0) {
      this.showFileError = true;
      return;
    }
    if(!this.fileUpload.files[0].name.endsWith(".hdf5")) {
      this.showfileFormatError = true;
      this.fileUpload.clear();
      return;
    }
    this.fileUpload.upload();
  }

  onBeforeUpload(event: any): void {
    event.formData.append("name", this.modelName);
  }

  onProgress(event: any): void {
    this.uploadProgress = event.progress;
    if(this.uploadProgress >= 100) {
      this.displayDialog = false;
    }
  }

  deleteModel(selectedModel: Model): void {
    this.modelOrchestrationService.deleteModel(selectedModel.id).subscribe(
      (data: any) => {
        this.models = this.models.filter(model => model.id != selectedModel.id)
        this.msgService.add({severity: "success", summary: `${selectedModel.id} has been deleted.`, detail: ""});
      },
      (data) => {
        console.log(data);
        let details = data.status < 500 ? data.error : "";
        this.msgService.add({severity: "error", summary: `Unable to delete model.`, detail: details});
      },
      () => {
        console.log("Completed");
      }
    );
  }

  activateModel(selectedModel: Model): void {
    this.modelOrchestrationService.activateModel(selectedModel.id).subscribe((data: any) => {
      selectedModel.active = true;
      this.msgService.add({severity: "success", summary: `${selectedModel.id} has been activated.`, detail: ""});
    },
    (data) => {
      console.log(data);
      let details = data.status < 500 ? data.error : "";
      this.msgService.add({severity: "error", summary: `Unable to activate model.`, detail: details});
    },
    () => {
      console.log("Completed");
    });
  }

  deactivateModel(selectedModel: Model): void {
    this.modelOrchestrationService.deactivateModel(selectedModel.id).subscribe((data: any) => {
      selectedModel.active = false;
      this.msgService.add({severity: "success", summary: `${selectedModel.id} has been deactivated.`, detail: ""});
    },
    (data) => {
      console.log(data);
      let details = data.status < 500 ? data.error : "";
      this.msgService.add({severity: "error", summary: `Unable to deactivate model.`, detail: details});
    },
    () => {
      console.log("Completed");
    });
  }

  updateModelList(): void {
    this.modelOrchestrationService.listModels().subscribe((data: any) => {
      this.models = data.models;
    });
  }

  showCreateDialog() {
    this.showNameError = false;
    this.showFileError = false;
    this.showfileFormatError = false;
    this.modelName = "";
    this.uploadProgress = 0;
    this.displayDialog = true;
  }

  getEventValue($event:any) :string {
    return $event.target.value;
  }
}
