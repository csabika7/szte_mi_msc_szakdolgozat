import { TestBed } from '@angular/core/testing';

import { ModelStorageService } from './model-storage.service';

describe('ModelStorageService', () => {
  let service: ModelStorageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ModelStorageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
