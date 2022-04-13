import { Model } from './model';

describe('Model', () => {
  it('should create an instance', () => {
    expect(new Model("123", "name", true)).toBeTruthy();
  });
});
