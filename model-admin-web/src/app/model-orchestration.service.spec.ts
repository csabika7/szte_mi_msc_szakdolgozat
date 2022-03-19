import { TestBed } from '@angular/core/testing';

import { ModelOrchestrationService } from './model-orchestration.service';

describe('ModelOrchestrationService', () => {
  let service: ModelOrchestrationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ModelOrchestrationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
