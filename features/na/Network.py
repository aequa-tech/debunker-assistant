from database import DomainsLabelDistribution, get_db
from fastapi import Dependse
from sqlalchemy.orm import Session

import tldextract


class Network():


    def get_backpropagation_untrustability(self, url, db: Session = Depends(get_db)):

        domain=tldextract.extract(url).registered_domain
        labelDistribution=db.query(DomainsLabelDistribution).filter(DomainsLabelDistribution.domain == domain).first()
        if labelDistribution is not None:
            result=round(labelDistribution.untrusted_norm,3)
            return    { "values" : {
                    "absolute": result,
                    "local": result,
                    "global": None,
                }}

        else:
            None
