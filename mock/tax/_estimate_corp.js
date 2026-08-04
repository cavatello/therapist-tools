function estimateCorp(c){
  /* Deliberately simple, and labelled as such: a professional corporation pays the
     owner a defensible salary and takes the rest as a distribution, which stops the
     Medicare portion but not the Social Security portion once salary clears the base.
     Netted against real running costs. */
  if (c.profit <= 0) return 0;
  var salary = Math.max(0, c.profit * .5);
  var seBase = c.profit * SE_FACTOR;
  var soleSE = OASDI * Math.min(seBase, SS_BASE) + MEDI * seBase;
  var corpSE = OASDI * Math.min(salary, SS_BASE) + MEDI * salary;
  var runCost = 600 * 12 / 12 + 1000 + 25 + 800;   /* payroll svc, 1120-S, SOI, franchise */
  runCost = 600 + 1000 + 25 + Math.max(800, c.profit * .015);
  return soleSE - corpSE - runCost;
}
