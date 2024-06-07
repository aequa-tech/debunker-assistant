from database import DomainsLabelDistribution
import tldextract


class Network():


    def get_backpropagation_untrustability(self, url, db):

        domain=tldextract.extract(url).registered_domain
        labelDistribution=db.query(DomainsLabelDistribution).filter(DomainsLabelDistribution.domain == domain).first()
        if labelDistribution is not None:
            result=round(labelDistribution.untrusted_norm,3)
            return    {     "description": "back propagation untrustability",
                "values" : {
                    "absolute": result,
                    "local_normalisation": result,
                    "global_normalisation": None,
                },
                'descriptions': {
                        'absolute': '',
                        'local_normalisation': '',
                        'global_normalisation': None
                }}

        else:
            None


