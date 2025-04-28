import { DistanceType } from "../../gen/run_pb";

export type Subscription = {
  id: number;
  cities: string[];
  distances: DistanceType[];
  tags: string[];
};
